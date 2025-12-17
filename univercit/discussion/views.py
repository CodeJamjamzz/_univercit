from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import connection
from .models import Forum, Thread, Comment

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

    # Get forum's threads
    forum_threads = forum.get_threads()

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
        thread_comments.append(Comment(**row_dict))

    thread_student = thread.get_student()

    # Give thread info to thread template
    return render(request, 'thread.html', {
        'thread': thread,
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

    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(
            content=content,
            thread_id=thread,
            student_id=request.user.id
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
    if request.method == 'POST':
        new_content = request.POST.get('edit_content')
        thread_id = Comment.objects.get(comment_id=comment_id).thread_id.thread_id

        success = False
        with connection.cursor() as cursor:
            cursor.callproc('edit_comment', [
                request.user.id,
                comment_id,
                new_content,
                success
            ])

    return redirect('thread', thread_id=thread_id)