# rating/views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST

# Import all the models you need to reference
from user.models import Student
from discussion.models import Comment, Thread
from file.models import File
from .models import CommentRating, FileRating, ThreadRating

type_sh = {
    'comment': (Comment, CommentRating),
    'file': (File, FileRating),
    'thread': (Thread, ThreadRating),
}

@login_required
@require_POST
def rate(request):
    try:
        if isinstance(request.user, Student):
            student = request.user
        else:
            student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return HttpResponseBadRequest('Student profile not found.')
    except Exception:
        return HttpResponseBadRequest('Could not find user.')

    # get details
    item_id = request.POST.get('item_id')
    item_type = request.POST.get('item_type')
    action = request.POST.get('action')
    next_url = request.POST.get('next', '/') # go to the url where u came from

    if not all([item_id, item_type, action]):
        return HttpResponseBadRequest('Missing parameters.')
    if item_type not in type_sh:
        return HttpResponseBadRequest('Invalid item_type.')

    # put details
    ItemModel, RatingModel = type_sh[item_type]
    item_fk_field = f"{item_type}Id"
    item = get_object_or_404(ItemModel, pk=item_id)

    filter_kwargs = {'studentId': student, item_fk_field: item}
    existing_rating = RatingModel.objects.filter(**filter_kwargs).first()
    # upvoting / downvoting logic
    if existing_rating:
        if action == 'upvote':
            if existing_rating.isUpvoted:
                existing_rating.delete()
            else:
                existing_rating.isUpvoted = True
                existing_rating.save()
        elif action == 'downvote':
            if not existing_rating.isUpvoted:
                existing_rating.delete()
            else:
                existing_rating.isUpvoted = False
                existing_rating.save()
    else:
        create_kwargs = {
            'studentId': student,
            item_fk_field: item,
            'isUpvoted': (action == 'upvote')
        }
        RatingModel.objects.create(**create_kwargs)
    return redirect(next_url)

class RatingView(View):
    def get(self, request):
        # Create mock thread object for title
        class MockThread:
            def __init__(self):
                self.threadTitle = 'How to mock POST requests'
                self.threadId = 1
                self.forumId = type('MockForum', (), {'forumId': 1})()
        
        thread = MockThread()
        
        # Create mock thread object with item structure for the card template
        class MockThreadItem:
            def __init__(self):
                self.content = 'How to mock POST requests'
                self.student_username = 'Student Username'
                self.item_id = thread.threadId
                self.item_type = 'thread'
                self.vote_count = 0
                self.user_vote = None  # 'upvote', 'downvote', or None
        
        thread_item = MockThreadItem()
        
        # Create mock comments with dummy data
        class MockComment:
            def __init__(self, content, username, comment_id, vote_count, user_vote):
                self.content = content
                self.student_username = username
                self.item_id = comment_id
                self.item_type = 'comment'
                self.vote_count = vote_count
                self.user_vote = user_vote  # 'upvote', 'downvote', or None
        
        # Dummy comments matching the image
        thread_comments = [
            MockComment('how to do this', 'Student Username', 1, 0, None),
            MockComment('no idea', 'Student Username', 2, 0, None),
            MockComment('just look it up in youtube', 'Student Username', 3, 0, None),
            MockComment('asdfawhaerehaerg', 'Student Username', 4, 0, None),
        ]
        
        context = {
            'thread': thread,
            'thread_item': thread_item,
            'thread_comments': thread_comments,
        }
        
        return render(request, 'rating.html', context)
