import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Student
from django.db import connection

# Create your views here.
def index(request):
    return render(request, 'index.html')
class DashboardView(View):
    template = 'dashboard.html'
    def get(self, request):
        return render(request, self.template)

class LogInView(View):
    template = "login.html"
    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        login_status = 0

        with connection.cursor() as cursor:
            cursor.execute("SET @login_result = 0;")
            cursor.execute("CALL user_login(%s, %s, @login_result);", [email, password])
            cursor.execute("SELECT @login_result;")
            login_status = cursor.fetchone()[0]

        if login_status == 1:
            request.session['user_email'] = email
            request.session['is_authenticated'] = True
            print("LOGIN")
            return redirect('/curriculum/programs/')

        else:
            print("DID NOT LOGIN")
            return render(request, "login.html", {"error": "Invalid credentials"})

class SignInView(View):
    template = "signin.html"

    def get_programs(self):

        with connection.cursor() as cursor:
            cursor.execute("Select * from all_programs")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            programs = [dict(zip(columns, row)) for row in rows]

        return programs

    def get(self, request):
        programs = self.get_programs()
        return render(request, self.template, {'programs': programs})

        # if not programs:
        #     programs = [{"program_code": "None", "program_desc": "No programs available"}]
        # return render(request, self.template, {'programs': programs})
    def post(self, request):
        programs = self.get_programs()
        program_code = request.POST.get("program_code")
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, self.template, {"error": "Passwords do not match.", 'programs': programs})
        if len(password) < 8:
            return render(request, self.template, {"error": "Password must be at least 8 characters long.", 'programs': programs})
        if not re.search(r"[A-Z]", password):
            return render(request, self.template,{"error": "Password must contain at least one uppercase letter.", 'programs': programs})
        if not re.search(r"[a-z]", password):
            return render(request, self.template,{"error": "Password must contain at least one lowercase letter.", 'programs': programs})
        if not re.search(r"[0-9]", password):
            return render(request, self.template,{"error": "Password must contain at least one number.", 'programs': programs})

        with connection.cursor() as cursor:
            cursor.callproc("user_signup", [
                program_code,
                firstname,
                lastname,
                username,
                email,
                password,
                confirm_password,
                None
            ])

            # Retrieve OUT parameter value
            cursor.execute("SELECT @_user_signup_7;")  # 7 is the index of OUT param (0-based)
            status = cursor.fetchone()[0]

            if status == 1:
                return render(request, self.template, {"error": "Account has already been used.", 'programs': programs})
            elif status == 2:
                return redirect('/curriculum/programs/')
            elif status == 3:
                return render(request, self.template, {"error": "Passwords does not match.", 'programs': programs})

