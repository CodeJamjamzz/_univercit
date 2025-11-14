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
        # Dummy data for demonstration
        context = {
            'comment_text': 'This is a sample comment that demonstrates the upvote/downvote system. You can click the buttons to see how they work!',
            'author': 'DemoUser',
            'vote_count': 42,
            'upvotes': 50,
            'downvotes': 8,
            'user_vote': None,  # Can be 'upvote', 'downvote', or None
            'item_id': 1,
            'item_type': 'comment',
        }
        
        return render(request, 'rating.html', context)
