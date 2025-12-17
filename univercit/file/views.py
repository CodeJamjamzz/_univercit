# Simple front-end for file upload
from django.views.decorators.csrf import csrf_exempt

def file_upload_form(request):
    """Render a simple file upload form."""
    return render(request, 'file_upload.html')
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST
from user.models import Student
from curriculum.models import Course
from .models import File
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # TODO: Remove csrf_exempt in production for security. See docs.
@require_POST
def submit(request):
    """
    Upload a file for a course (no login required).
    TODO: Make course required again when ready. Currently optional for testing/demo.
    """
    # get details
    course_id = request.POST.get('course_id')
    file_obj = request.FILES.get('file')
    file_desc = request.POST.get('file_desc', '')
    next_url = request.POST.get('next', '/')  # return to previous page

    if not file_obj:
        return HttpResponseBadRequest('Missing file.')

    # TODO: Make course required again. For now, allow uploads without a course (for testing/demo).
    course = None
    if course_id:
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            course = None

    # Get student
    student_id = None
    if request.user.is_authenticated:
        try:
            # Check if user is already a Student instance (custom auth) or related
            if hasattr(request.user, 'student'):
                student_id = request.user.student.student_id
            else:
                 # Fallback/Safety if Student model is linked differently
                 student = Student.objects.get(user=request.user)
                 student_id = student.student_id
        except Student.DoesNotExist:
            pass # Handle non-student users (admin?) gracefully or let DB error

    # Call stored procedure to add file
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.callproc('add_file', [
            course.pk if course else None,
            student_id,
            str(file_obj), # file_url 
            file_desc,
            1 # is_visible=True
        ])

    return redirect(next_url)

class FileView(View):
    """Lists all uploaded files for manual viewing (for demo/testing)."""
    def get(self, request):
        files = File.objects.filter(is_visible=True)
        return render(request, 'file.html', {'files': files})

@csrf_exempt
def delete_file(request, file_id):
    """Delete a file."""
    student_id = None 
    if request.user.is_authenticated:
        try:
            if hasattr(request.user, 'student'):
                student_id = request.user.student.student_id
            else:
                 student = Student.objects.get(user=request.user)
                 student_id = student.student_id
        except Student.DoesNotExist:
            pass 

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.callproc('delete_file', [
            file_id,
            student_id
        ])
    
    return redirect('fileView')
