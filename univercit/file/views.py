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

    File.objects.create(
        student_id=None,
        course_id=course,
        file_url=file_obj,
        file_desc=file_desc,
        is_visible=True
    )

    return redirect(next_url)

class FileView(View):
    """Lists all uploaded files for manual viewing (for demo/testing)."""
    def get(self, request):
        files = File.objects.filter(is_visible=True)
        return render(request, 'file.html', {'files': files})
