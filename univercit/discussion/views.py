from django.shortcuts import render
from django.http import HttpResponse
from .models import Forum, Thread

# Create your views here.
def forum_view(request, forum_id):
    # Get forum based on ID in url
    forum = Forum.objects.get(forumId=forum_id)
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

def thread_view(request, thread_id):
    return HttpResponse(
        """
        yo
        """
    )