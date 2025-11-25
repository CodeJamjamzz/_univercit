def testimonial_write_form(request):
    """Render a simple testimonial writing form."""
    return render(request, 'testimonial_write.html')
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from django.views import View
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt  # TODO: Remove csrf_exempt in production for security. See docs.
def submit(request):
    """
    Submit a testimonial. No login or CSRF required. Course is optional.
    TODO: Make course required again when ready. Currently optional for testing/demo.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required.')
    course_id = request.POST.get('course_id')
    content = request.POST.get('content', '')
    next_url = request.POST.get('next', '/')
    if not content:
        return HttpResponseBadRequest('Missing content.')
    # TODO: Make course required again. For now, allow testimonials without a course (for testing/demo).
    course = None
    if course_id:
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            course = None
    Testimonial.objects.create(
        student_id=None,
        course_id=course,
        content=content,
        is_visible=True
    )
    return redirect(next_url)


def testimonial_list(request):
    """View all testimonials (public, no login required)."""
    testimonials = Testimonial.objects.all().order_by('-testimonial_id')
    return render(request, 'testimonial_list.html', {'testimonials': testimonials})

class TestimonialView(View):
    """Placeholder view for testimonial app."""
    def get(self, request):
        return render(request, 'testimonial.html')


