# user/middleware.py
from user.models import Student


class SwapUserToStudentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:

                student = Student.objects.get(email=request.user.email)

                student.is_authenticated = True
                student.is_staff = request.user.is_staff
                student.is_superuser = request.user.is_superuser
                student.backend = getattr(request.user, 'backend', 'django.contrib.auth.backends.ModelBackend')

                request.user = student

            except Student.DoesNotExist:
                pass

        return self.get_response(request)