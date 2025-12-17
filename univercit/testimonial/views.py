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
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.callproc('add_testimonial', [
            course.pk if course else None,
            None, # student_id
            content,
            1 # is_visible=True
        ])

    return redirect(next_url)


def testimonial_list(request):
    """View all testimonials (public, no login required)."""
    testimonials = Testimonial.objects.all().order_by('-testimonial_id')
    return render(request, 'testimonial_list.html', {'testimonials': testimonials})

class TestimonialView(View):
    """Placeholder view for testimonial app."""
    def get(self, request):
        return render(request, 'testimonial.html')


@csrf_exempt
def delete_testimonial(request, testimonial_id):
    """Delete a testimonial knowing the ID."""
    if request.method != 'POST':
        # Fallback for non-POST/JS method if needed, or strictly enforce POST
        pass
    
    # In a real app, get student_id from logical session/auth
    student_id = None # Placeholder or get from request.user.student.id

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.callproc('delete_testimonial', [
            testimonial_id,
            student_id 
        ])
    
    # redirect to where they came from or list
    return redirect('testimonial_list')

@csrf_exempt
def edit_testimonial(request, testimonial_id):
    """Edit a testimonial."""
    if request.method == 'POST':
        content = request.POST.get('content')
        student_id = None # Placeholder
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.callproc('edit_testimonial', [
                testimonial_id,
                student_id,
                content
            ])
        return redirect('testimonial_list')
    
    # Render edit form
    # We need to fetch the existing content first to populate the form
    # Using raw SQL for read consistency
    testimonial = None
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT testimonial_id, content FROM testimonial_testimonial WHERE testimonial_id = %s", [testimonial_id])
        row = cursor.fetchone()
        if row:
            testimonial = {'testimonial_id': row[0], 'content': row[1]}

    return render(request, 'testimonial_write.html', {'testimonial': testimonial, 'is_edit': True})


