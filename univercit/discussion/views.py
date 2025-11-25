from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Forum, Thread, Comment

from datetime import datetime

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
    # TODO: paginate
    thread_comments = thread.get_comments()
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

        thread = Thread.objects.create(
            forum_id=forum,
            thread_title=thread_title,
            date_created=datetime.now(),
            student_id=request.user.id
        )
        return redirect('thread', thread_id=thread.thread_id)

    return redirect('forum', forum_id=forum_id)

def add_comment(request, thread_id):
    # Reject comment if user not auth
    # if not request.user.is_authenticated():
    #     return

    thread = Thread.objects.get(thread_id=thread_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(
            content=content,
            thread_id=thread,
            student_id=request.user.id
        )
    return redirect('thread', thread_id=thread_id)