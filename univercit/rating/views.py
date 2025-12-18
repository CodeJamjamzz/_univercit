from django.shortcuts import redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from user.models import Student

@login_required
@require_POST
def rate(request):
    # getting user
    user_email = request.user.email
    if not user_email:
        student = None
    else:
        try:
            student = Student.objects.get(email__iexact=user_email)
        except Student.DoesNotExist:
            student = None
        except Student.MultipleObjectsReturned:
            student = Student.objects.filter(email__iexact=user_email).first()

    # getting params
    item_id = request.POST.get('item_id')
    item_type = request.POST.get('item_type')
    action = request.POST.get('action')
    next_url = request.POST.get('next', '/')

    # stored proc calling
    with connection.cursor() as cursor:
        cursor.callproc('Rate', [student.id, item_id, item_type, action])

    return redirect(next_url)