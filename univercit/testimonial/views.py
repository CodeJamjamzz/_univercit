from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST
from user.models import Student
from curriculum.models import Course
from .models import Testimonial

"""
Testimonial Backend Service
--------------------------
This app provides backend services for handling course testimonials.
It does not provide its own interface, but instead is meant to be used through forms
embedded in other templates (primarily course detail pages).

Example Usage in Templates:
    <form method="POST" action="{% url 'testimonial:submit' %}">
        {% csrf_token %}
        <input type="hidden" name="course_id" value="{{ course.course_id }}">
        <input type="hidden" name="next" value="{{ request.path }}">
        <textarea name="content" required placeholder="Write your testimonial"></textarea>
        <button type="submit">Submit Testimonial</button>
    </form>

Required Parameters:
- course_id: ID of the course the testimonial is for
- content: The testimonial text
- next (optional): URL to redirect to after submission (defaults to '/')

Security:
- Requires authenticated user
- Validates user has student profile
- Only accepts POST requests
- Associates testimonials with specific courses and students
"""

@login_required
@require_POST
def submit(request):
    """Submit a testimonial for a course."""
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
    course_id = request.POST.get('course_id')
    content = request.POST.get('content')
    next_url = request.POST.get('next', '/')  # return to previous page

    if not all([course_id, content]):
        return HttpResponseBadRequest('Missing parameters.')

    # Create testimonial
    course = get_object_or_404(Course, pk=course_id)
    Testimonial.objects.create(
        student_id=student,
        course_id=course,
        content=content,
        is_visible=True
    )

    return redirect(next_url)

class TestimonialView(View):
    """Placeholder view for testimonial app."""
    def get(self, request):
        return render(request, 'testimonial.html')
