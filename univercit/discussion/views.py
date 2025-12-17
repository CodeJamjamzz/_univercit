from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import connection
from django.db.models import Count, Q, F, Value, IntegerField, OuterRef, Subquery

from user.models import Student
from .models import Forum, Thread, Comment
from rating.models import ThreadRating

from datetime import datetime

from curriculum.models import Course


# Create your views here.
# @login_required
def forum_view(request, forum_id):
    # Get forum based on ID in url
    forum = Forum.objects.get(forum_id=forum_id)
    # Give 'page not found error' if forum does not exist
    if not forum:
        return HttpResponse("i dunno where that forum is")

    # Get student for vote status check
    # Assuming request.user.id maps to studentId as seen in other views
    try:
        student = Student.objects.get(studentId=request.user.id)
    except Student.DoesNotExist:
        student = None

    # Get forum's threads with dynamic scoring
    # Note: get_threads() returns a QuerySet, so we can chain annotations
    
    user_vote_subquery = ThreadRating.objects.filter(
        threadId=OuterRef('pk'),
        studentId=student
    ).values('isUpvoted')[:1]

    forum_threads = forum.get_threads().annotate(
        upvotes=Count('threadrating', filter=Q(threadrating__isUpvoted=True)),
        downvotes=Count('threadrating', filter=Q(threadrating__isUpvoted=False))
    ).annotate(
        score=F('upvotes') - F('downvotes'),
        user_is_upvoted=Subquery(user_vote_subquery)
    )

    # Give forum info to forum template
    return render(request, 'forum.html', {
        'forum': forum,
        'forum_threads': forum_threads
    })

# @login_required
def thread_view(request, thread_id):
    # Get thread based on ID in url
    thread = Thread.objects.get(thread_id=thread_id)
    # Give 'page not found error' if thread does not exist
    if not thread:
        return HttpResponse("i dunno where that thread is")

    # Get student for vote status check
    try:
        student = Student.objects.get(studentId=request.user.id)
    except Student.DoesNotExist:
        student = None

    # Annotate thread with vote scores and user status
    from rating.models import ThreadRating, CommentRating
    
    thread_vote_subquery = ThreadRating.objects.filter(
        threadId=thread.pk,
        studentId=student
    ).values('isUpvoted')[:1]

    annotated_thread = Thread.objects.filter(pk=thread.pk).annotate(
        upvotes=Count('threadrating', filter=Q(threadrating__isUpvoted=True)),
        downvotes=Count('threadrating', filter=Q(threadrating__isUpvoted=False))
    ).annotate(
        score=F('upvotes') - F('downvotes'),
        user_is_upvoted=Subquery(thread_vote_subquery)
    ).first()

    # Get thread's comments
    # TODO: add pagination in frontend
    current_page = 1

    with connection.cursor() as cursor:
        cursor.callproc('get_thread_comments', [
            thread_id,
            current_page
        ])
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    thread_comments = []
    for row in result:
        row_dict = dict(zip(columns, row))
        comment = Comment(**row_dict)
        
        # Annotate each comment with vote scores and user status
        comment_vote_subquery = CommentRating.objects.filter(
            commentId=comment.pk,
            studentId=student
        ).values('isUpvoted')[:1]
        
        annotated_comment = Comment.objects.filter(pk=comment.pk).annotate(
            upvotes=Count('commentrating', filter=Q(commentrating__isUpvoted=True)),
            downvotes=Count('commentrating', filter=Q(commentrating__isUpvoted=False))
        ).annotate(
            score=F('upvotes') - F('downvotes'),
            user_is_upvoted=Subquery(comment_vote_subquery)
        ).first()
        
        thread_comments.append(annotated_comment)

    thread_student = annotated_thread.get_student().username

    # Give thread info to thread template
    return render(request, 'thread.html', {
        'thread': annotated_thread,
        'thread_comments': thread_comments,
        'thread_student': thread_student
    })

# @login_required
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
    # Get thread_id first (needed for redirect)
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