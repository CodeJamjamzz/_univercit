import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Student
from django.db import connection


# Create your views here.
def index(request):
    return render(request, 'index.html')


def get_dashboardstatsrow():
    with connection.cursor() as cursor:
        cursor.callproc(
            'dashboard_getstatsrow',
            [0, 0, 0, 0, 0]
        )

        # Fetch ALL OUT parameters
        cursor.execute("""
            SELECT
                @_dashboard_getstatsrow_0,  -- total_students
                @_dashboard_getstatsrow_1,  -- total_programs
                @_dashboard_getstatsrow_2,  -- total_courses
                @_dashboard_getstatsrow_3,  -- total_files
                @_dashboard_getstatsrow_4;  -- status
        """)

        (
            total_students,
            total_programs,
            total_courses,
            total_files,
            status
        ) = cursor.fetchone()

    return {
        "total_students": total_students,
        "total_programs": total_programs,
        "total_courses": total_courses,
        "total_files": total_files,
        "status": status
    }


def dashboard_view():
    with connection.cursor() as cursor:
        cursor.callproc('chart_studentperprogram')
        rows = cursor.fetchall()

    total_students = sum(row[1] for row in rows) or 1

    program_stats = [
        {
            "program_name": row[0],
            "student_count": row[1],
            "student_pct": round((row[1] / total_students) * 100, 1)
        }
        for row in rows
    ]

    return program_stats

def get_courses_per_program():
    with connection.cursor() as cursor:
        cursor.callproc('chart_courseperprogram')
        rows = cursor.fetchall()  # list of tuples: (program_code, program_name, course_count)

    total_courses = sum(row[2] for row in rows) or 1

    program_stats = [
        {
            "program_code": row[0],
            "program_name": row[1],
            "course_count": row[2],
            "course_pct": round((row[2] / total_courses) * 100, 1)
        }
        for row in rows
    ]

    return program_stats

class DashboardView(View):
    template = 'dashboard.html'

    def get(self, request):
        data = get_dashboardstatsrow()
        total_students = data["total_students"]
        total_programs = data["total_programs"]
        total_courses = data["total_courses"]
        total_files = data["total_files"]
        status = int(data["status"])

        students_per_program = dashboard_view()
        course_per_program = get_courses_per_program()

        if status == 1:
            print("SQLExcetpion occured")
            return render(request, self.template)

        return render(request, self.template,
                      {"total_students": total_students,
                       "total_programs": total_programs,
                       "total_courses": total_courses,
                       "total_files": total_files,
                       "program_stats": students_per_program,
                       "courseperprogram_stats": course_per_program})


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
            try:
                student = Student.objects.filter(email=email).first()
                if student:
                   username = student.username
                else:
                   username = email.split('@')[0] # Fallback

                user, created = User.objects.get_or_create(username=username, defaults={'email': email})
                if created:
                    user.set_unusable_password()
                    user.save()

                if student and student.user != user:
                    student.user = user
                    student.save()

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                request.session['user_email'] = email
                request.session['is_authenticated'] = True
                print("LOGIN")
                return redirect('/curriculum/programs/')
            except Exception as e:
                print(f"Error syncing user: {e}")
                return render(request, "login.html", {"error": "Login Error"})

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
        program_code = request.POST.get("programId")
        print(program_code)
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, self.template, {"error": "Passwords do not match.", 'programs': programs})
        if len(password) < 8:
            return render(request, self.template,
                          {"error": "Password must be at least 8 characters long.", 'programs': programs})
        if not re.search(r"[A-Z]", password):
            return render(request, self.template,
                          {"error": "Password must contain at least one uppercase letter.", 'programs': programs})
        if not re.search(r"[a-z]", password):
            return render(request, self.template,
                          {"error": "Password must contain at least one lowercase letter.", 'programs': programs})
        if not re.search(r"[0-9]", password):
            return render(request, self.template,
                          {"error": "Password must contain at least one number.", 'programs': programs})

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
                # Sync with Django User
                try:
                    user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'first_name': firstname, 'last_name': lastname})
                    if created:
                        user.set_unusable_password()
                        user.save()
                    
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('/curriculum/programs/')
                except Exception as e:
                     print(f"Error syncing user: {e}")
                     return render(request, self.template, {"error": "Signup Error", 'programs': programs})

            elif status == 3:
                return render(request, self.template, {"error": "Passwords does not match.", 'programs': programs})
