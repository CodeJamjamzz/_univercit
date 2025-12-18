from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import connection
from django.db.models import Count, Q, F, Value, OuterRef, Subquery, BooleanField, Case, When, Exists
from datetime import datetime

from user.models import Student
from .models import Forum, Thread, Comment
from curriculum.models import Course
from rating.models import ThreadRating, CommentRating


# @login_required
def forum_view(request, forum_id):
    # Get forum based on ID in url
    forum = Forum.objects.get(forum_id=forum_id)
    if not forum:
        return HttpResponse("i dunno where that forum is")

    student = None
    if request.user.is_authenticated and request.user.email:
        try:
            # Case-insensitive email match
            student = Student.objects.filter(email__iexact=request.user.email).first()
        except Exception as e:
            print(f"Error finding student: {e}")
            student = None

    student_pk = student.studentId if student else None

    forum_threads = forum.get_threads().annotate(
        upvotes=Count('threadrating', filter=Q(threadrating__isUpvoted=True)),
        downvotes=Count('threadrating', filter=Q(threadrating__isUpvoted=False))
    ).annotate(
        score=F('upvotes') - F('downvotes'),
        user_is_upvoted=Case(
            When(Exists(ThreadRating.objects.filter(
                threadId=OuterRef('pk'),
                studentId_id=student_pk,
                isUpvoted=True
            )), then=Value(True)),

            When(Exists(ThreadRating.objects.filter(
                threadId=OuterRef('pk'),
                studentId_id=student_pk,
                isUpvoted=False
            )), then=Value(False)),

            default=None,
            output_field=BooleanField(null=True)
        )
    )

    return render(request, 'forum.html', {
        'forum': forum,
        'forum_threads': forum_threads
    })


# @login_required
def thread_view(request, thread_id):
    # 1. Get Thread
    thread = Thread.objects.get(thread_id=thread_id)
    if not thread:
        return HttpResponse("i dunno where that thread is")

    # 2. Get Student (ROBUST WAY: Match by Email)
    student = None
    if request.user.is_authenticated and request.user.email:
        try:
            student = Student.objects.filter(email__iexact=request.user.email).first()
        except Exception:
            student = None

    # Get the raw ID for safe database lookup
    student_pk = student.studentId if student else None

    # 3. Annotate Main Thread
    annotated_thread = Thread.objects.filter(pk=thread.pk).annotate(
        upvotes=Count('threadrating', filter=Q(threadrating__isUpvoted=True)),
        downvotes=Count('threadrating', filter=Q(threadrating__isUpvoted=False))
    ).annotate(
        score=F('upvotes') - F('downvotes'),
        user_is_upvoted=Case(
            When(Exists(ThreadRating.objects.filter(
                threadId=OuterRef('pk'),
                studentId_id=student_pk,  # explicit ID check
                isUpvoted=True
            )), then=Value(True)),

            When(Exists(ThreadRating.objects.filter(
                threadId=OuterRef('pk'),
                studentId_id=student_pk,  # explicit ID check
                isUpvoted=False
            )), then=Value(False)),

            default=None,
            output_field=BooleanField(null=True)
        )
    ).first()

    current_page = 1
    with connection.cursor() as cursor:
        cursor.callproc('get_thread_comments', [thread_id, current_page])
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    thread_comments = []
    for row in result:
        row_dict = dict(zip(columns, row))
        comment = Comment(**row_dict)

        # Annotate each comment with vote status
        annotated_comment = Comment.objects.filter(pk=comment.pk).annotate(
            upvotes=Count('commentrating', filter=Q(commentrating__isUpvoted=True)),
            downvotes=Count('commentrating', filter=Q(commentrating__isUpvoted=False))
        ).annotate(
            score=F('upvotes') - F('downvotes'),
            user_is_upvoted=Case(
                When(Exists(CommentRating.objects.filter(
                    commentId=comment.pk,
                    studentId_id=student_pk,  # explicit ID check
                    isUpvoted=True
                )), then=Value(True)),

                When(Exists(CommentRating.objects.filter(
                    commentId=comment.pk,
                    studentId_id=student_pk,  # explicit ID check
                    isUpvoted=False
                )), then=Value(False)),

                default=None,
                output_field=BooleanField(null=True)
            )
        ).first()

        thread_comments.append(annotated_comment)

    thread_student = annotated_thread.get_student().username if annotated_thread else "Unknown"

    return render(request, 'thread.html', {
        'thread': annotated_thread,
        'thread_comments': thread_comments,
        'thread_student': thread_student
    })


# @login_required
def add_thread(request, forum_id):
    if request.method == 'POST':
        forum = Forum.objects.get(forum_id=forum_id)
        thread_title = request.POST.get('threadTitle')
        thread_first_comment = request.POST.get('threadFirstComment')

        with connection.cursor() as cursor:
            cursor.callproc('add_thread', [
                forum.forum_id,
                thread_title,
                thread_first_comment,
                request.user.id
            ])
            thread_id = cursor.fetchone()[0]

        thread = Thread.objects.get(thread_id=thread_id)

        return redirect('thread', thread_id=thread.thread_id)

    return redirect('forum', forum_id=forum_id)


# @login_required
def add_comment(request, thread_id):
    thread = Thread.objects.get(thread_id=thread_id)
    student = Student.objects.get(studentId=request.user.id)

    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(
            content=content,
            thread_id=thread,
            student_id=student
        )
    return redirect('thread', thread_id=thread_id)


# @login_required
def all_forums_view(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return HttpResponse("Course ID is required.", status=400)

    course = get_object_or_404(Course, course_id=course_id)
    forums = Forum.objects.filter(course_id=course)

    return render(request, 'all_forums.html', {
        'course': course,
        'forums': forums
    })


# @login_required
def add_reply(request, comment_id):
    comment = Comment.objects.get(comment_id=comment_id)
    thread = comment.thread_id

    if request.method == 'POST':
        reply = request.POST.get('reply_content')
        Comment.objects.create(
            content=reply,
            thread_id=thread,
            student_id=request.user.id,
            reply_to=comment
        )

    return redirect('thread', thread_id=thread.thread_id)


# @login_required
def edit_comment(request, comment_id):
    comment = Comment.objects.get(comment_id=comment_id)
    thread_id = comment.thread_id.thread_id

    if request.method == 'POST':
        new_content = request.POST.get('edit_content')

        success = False
        with connection.cursor() as cursor:
            cursor.callproc('edit_comment', [
                request.user.id,
                comment_id,
                new_content,
                success
            ])

    return redirect('thread', thread_id=thread_id)