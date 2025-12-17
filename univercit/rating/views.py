from django.shortcuts import redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from user.models import Student

@login_required
@require_POST
def rate(request):
    # getting user
    student = request.user if isinstance(request.user, Student) else Student.objects.get(user=request.user)

    # getting params
    item_id = request.POST.get('item_id')
    item_type = request.POST.get('item_type')
    action = request.POST.get('action')
    next_url = request.POST.get('next', '/')

    # stored proc calling
    with connection.cursor() as cursor:
        cursor.callproc('Rate', [student.id, item_id, item_type, action])

    return redirect(next_url)