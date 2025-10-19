from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST
from user.models import Student
from curriculum.models import Course
from .models import File

"""
File Upload Backend Service
--------------------------
This app provides backend services for handling file uploads within course pages.
It does not provide its own interface, but instead is meant to be used through forms
embedded in other templates (primarily course detail pages).

Example Usage in Templates:
    <form method="POST" action="{% url 'file:submit' %}" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="hidden" name="course_id" value="{{ course.course_id }}">
        <input type="hidden" name="next" value="{{ request.path }}">
        <input type="file" name="file" required>
        <textarea name="file_desc" placeholder="File description"></textarea>
        <button type="submit">Upload File</button>
    </form>

Required Parameters:
- course_id: ID of the course the file belongs to
- file: The actual file being uploaded
- next (optional): URL to redirect to after upload (defaults to '/')
- file_desc (optional): Description of the file

Security:
- Requires authenticated user
- Validates user has student profile
- Only accepts POST requests
- Associates files with specific courses and students
"""

@login_required
@require_POST
def submit(request):
    """Upload a file for a course."""
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
    file_obj = request.FILES.get('file')
    file_desc = request.POST.get('file_desc', '')
    next_url = request.POST.get('next', '/')  # return to previous page

    if not all([course_id, file_obj]):
        return HttpResponseBadRequest('Missing parameters.')

    # Upload file
    course = get_object_or_404(Course, pk=course_id)
    File.objects.create(
        student_id=student,
        course_id=course,
        file_url=file_obj,
        file_desc=file_desc,
        is_visible=True
    )

    return redirect(next_url)

class FileView(View):
    """Placeholder view for file app."""
    def get(self, request):
        return render(request, 'file.html')
