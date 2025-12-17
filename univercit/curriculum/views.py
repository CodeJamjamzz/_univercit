# curriculum/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.db.models import Q, Count, Sum, F
from django.db.models.functions import Coalesce

from .models import Program, Course
from discussion.models import Forum
from file.models import File
from .utils import *

# Program Views

# Limit the program the can be seen by the User on what program they are in
class ProgramListView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        query = request.GET.get('query', '')

        programs = get_programs(query)

        return render(request, "all-programs.html", {
            "programs": programs
        })
    
class DashboardProgramListView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        programs = get_programs()

        return render(request, "dashboard-programs.html", {
            "programs": programs
        })

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class ProgramDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, program_code):
        program = get_object_or_404(Program, program_code=program_code)
        query = request.GET.get('query', '')
        if query:
            query = query.strip()
            courses = program.courses.filter(
                Q(course_id__icontains=query) | Q(course_name__icontains=query)
            )
        else:
            courses = program.courses.all()

        program = get_object_or_404(Program, pk=program_code)
        return render(request, 'program.html', {
            "program": program,
            "courses": courses
        })


class ProgramCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'

    def post(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to create programs.")
        
        action = request.POST.get('action')
        
        if action == "discard":
            return redirect(reverse_lazy("dashboard_program_list"))
        
        program_code = request.POST.get('program-code', '').strip()
        program_name = request.POST.get('program-name', '').strip()
        program_desc = request.POST.get('program-desc', '').strip()
        program_courses = request.POST.get('courses-selected', '').strip()

        error_list = []
        if program_code == "":
            error_list.append("Program Code")
        if program_name == "":
            error_list.append("Program Name")
        if program_desc == "":
            error_list.append("Program Description")

        if len(error_list) != 0:
            error_msg = "Submission Error: Empty " + ", ".join(error_list)
            messages.error(request, error_msg)
            return render(request, 'dashboard-program-form.html', {
                "courses": Course.objects.all(),
                "mode": "create",
                "form_values": {
                    "program_code": program_code,
                    "program_name": program_name,
                    "program_desc": program_desc,
                    "program_courses": program_courses.split(",")
                },
                "error_msg": error_msg
            })

        status = create_program(program_code, program_name, program_desc, program_courses)

        if not status["success"]:
            messages.error(request, status["error"])
            return render(request, 'dashboard-program-form.html', {
                "courses": Course.objects.all(),
                "mode": "create",
                "form_values": {
                    "program_code": program_code,
                    "program_name": program_name,
                    "program_desc": program_desc,
                    "program_courses": program_courses.split(",")
                },
            })
        else:
            messages.success(request, f"Program {program_code} created successfully!")
            if action == "create":
                return redirect(reverse_lazy("dashboard_program_list"))
            elif action == "create-add":
                return redirect(reverse_lazy("dashboard_program_create"))

        return redirect(reverse_lazy("dashboard_program_list"))
        
    
    def get(self, request):
        return render(request, 'dashboard-program-form.html', {
            "courses": Course.objects.all(),
            "mode": "create"
        })


    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class ProgramUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'
    
    def post(self, request, program_code):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to create programs.")
        
        action = request.POST.get('action')
        
        if action == "discard":
            return redirect(reverse_lazy("dashboard_program_list"))
        
        program = get_object_or_404(Program, program_code=program_code)
        program_name = request.POST.get('program-name', '').strip()
        program_desc = request.POST.get('program-desc', '').strip()
        program_courses = request.POST.get('courses-selected', '').strip()

        error_list = []
        if program_name == "":
            error_list.append("Program Name")
        if program_desc == "":
            error_list.append("Program Description")

        if len(error_list) != 0:
            error_msg = "Submission Error: Empty " + ", ".join(error_list)
            messages.error(request, error_msg)
            return render(request, 'dashboard-program-form.html', {
                "program": program,
                "courses": Course.objects.all(),
                "mode": "update",
                "form_values": {
                    "program_code": program_code,
                    "program_name": program_name,
                    "program_desc": program_desc,
                    "program_courses": program_courses.split(",")
                },
            })

        status = update_program(
            program_code, program_name, program_desc, program_courses
        )

        if not status["success"]:
            messages.error(request, status["error"])
            return render(request, 'dashboard-program-form.html', {
                "courses": Course.objects.all(),
                "mode": "create",
                "form_values": {
                    "program_code": program_code,
                    "program_name": program_name,
                    "program_desc": program_desc,
                    "program_courses": program_courses.split(",")
                },
            })
        else:
            messages.success(request, f"Program {program_code} updated successfully!")
            if action == "create":
                return redirect(reverse_lazy("dashboard_program_list"))
            elif action == "save-edit":
                return redirect(reverse_lazy("dashboard_program_update", args=(program_code,)))


    def get(self, request, program_code):
        program = get_object_or_404(Program, program_code=program_code)
        return render(request, 'dashboard-program-form.html', {
            "program": program,
            "courses": Course.objects.all(),
            "mode": "update"
        })
    

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    

class ProgramDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'

    def post(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowd to delete programs.")
        
        programs = request.POST.get('selected-programs-delete', '').strip()

        if programs == "" or programs is None:
            return redirect(reverse_lazy('dashboard_program_list'))

        programs_selected = programs.split(',')

        for code in programs_selected:
            status = delete_program(code)

            if not status["success"]:
                messages.error(request, status["error"])
                return redirect(reverse_lazy('dashboard_program_list'))

        if (len(programs_selected) > 4):
            messages.success(request, f"Programs {", ".join(programs_selected[:4])}, and {len(programs_selected) - 4} others deleted successfully!")
        elif (len(programs_selected) == 1):
            messages.success(request, f"Program {programs_selected[0]} deleted successfully!")
        else:
            messages.success(request, f"Programs {", ".join(programs_selected)} deleted successfully!")

        return redirect(reverse_lazy('dashboard_program_list'))
    

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


# Course Views
class CourseListView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        query = request.GET.get('query', '')

        courses = get_courses(query)

        for course in courses:
            programs = get_courses_programs(course["course_id"])
            course["programs"] = programs

        return render(request, "all-courses.html", {
            "courses": courses,
        })


class DashboardCourseListView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        courses = get_courses()

        return render(request, "dashboard-courses.html", {
            "courses": courses
        })
    

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class CourseDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    
    def get(self, request, course_id):
        course = get_course(course_id)
        programs = get_courses_programs(course_id)

        top_files = File.objects.filter(course_id=course_id).annotate(
            popularity_score=F('upvote_count') - F('downvote_count')
        ).order_by('-popularity_score')[:5]

        top_forums = Forum.objects.filter(course_id=course_id).annotate(
            thread_count=Count('thread'),
            total_upvotes=Coalesce(Sum('thread__upvote_count'), 0)
        ).annotate(
                popularity_score=F('thread_count') + F('total_upvotes')
        ).order_by('-popularity_score')[:5]

        return render(request, 'course.html', {
            "programs": programs,
            "course": course,
            "files": top_files,
            "forums": top_forums
        })


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'

    def post(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to create courses.")
        
        action = request.POST.get('action')
        
        if action == "discard":
            return redirect(reverse_lazy("dashboard_course_list"))
        
        course_id = request.POST.get('course-id', '').strip()
        course_name = request.POST.get('course-name', '').strip()
        course_desc = request.POST.get('course-desc', '').strip()
        course_programs = request.POST.get('programs-selected', '').strip()

        error_list = []
        if course_id == "":
            error_list.append("Course ID")
        if course_name == "":
            error_list.append("Course Name")
        if course_desc == "":
            error_list.append("Course Description")
        if course_programs == "":
            error_list.append("Program")

        if len(error_list) != 0:
            error_msg = "Submission Error: Empty " + ", ".join(error_list)
            messages.error(request, error_msg)
            return render(request, 'dashboard-course-form.html', {
                "programs": Program.objects.all(),
                "mode": "create",
                "form_values": {
                    "course_id": course_id,
                    "course_name": course_name,
                    "course_desc": course_desc,
                    "course_programs": course_programs.split(",")
                },
            })

        status = create_course(course_id, course_name, course_desc, course_programs)

        if not status["success"]:
            messages.error(request, status["error"])
            return render(request, 'dashboard-course-form.html', {
                "programs": Program.objects.all(),
                "mode": "create",
                "form_values": {
                    "course_id": course_id,
                    "course_name": course_name,
                    "course_desc": course_desc,
                    "course_programs": course_programs.split(",")
                },
            })
        else:
            messages.success(request, f"Course {course_id} created successfully!")
            if action == "create":
                return redirect(reverse_lazy("dashboard_course_list"))
            elif action == "create-add":
                return redirect(reverse_lazy("dashboard_course_create"))
        
        return redirect(reverse_lazy("dashboard_course_list"))
    

    def get(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to create courses.")
        
        return render(request, "dashboard-course-form.html", {
            "programs": Program.objects.all(),
            "mode": "create",
        })
    

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'

    def post(self, request, course_id):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to update courses.")
        
        action = request.POST.get('action')
        
        if action == "discard":
            return redirect(reverse_lazy("dashboard_course_list"))
        
        course = get_object_or_404(Course, course_id=course_id)
        course_name = request.POST.get('course-name', '').strip()
        course_desc = request.POST.get('course-desc', '').strip()
        course_programs = request.POST.get('programs-selected', '').strip()

        error_list = []
        if course_name == "":
            error_list.append("Course Name")
        if course_desc == "":
            error_list.append("Course Description")
        if course_programs == "":
            error_list.append("Program")

        if len(error_list) != 0:
            error_msg = "Submission Error: Empty " + ", ".join(error_list)
            messages.error(request, error_msg)
            return render(request, 'dashboard-course-form.html', {
                "course": course,
                "programs": Program.objects.all(),
                "mode": "update",
                "form_values": {
                    "course_id": course_id,
                    "course_name": course_name,
                    "course_desc": course_desc,
                    "course_programs": course_programs.split(",")
                },
            })

        status = update_course(course_id, course_name, course_desc, course_programs)

        if not status["success"]:
            messages.error(request, status["error"])
            return render(request, 'dashboard-course-form.html', {
                "course": course,
                "programs": Program.objects.all(),
                "mode": "update",
                "form_values": {
                    "course_id": course_id,
                    "course_name": course_name,
                    "course_desc": course_desc,
                    "course_programs": course_programs.split(",")
                },
            })
        else:
            messages.success(request, f"Course {course_id} updated successfully!")
            if action == "create":
                return redirect(reverse_lazy("dashboard_course_list"))
            elif action == "save-edit":
                return redirect(reverse_lazy("dashboard_course_update", args=(course_id,)))

        return redirect(reverse_lazy("dashboard_course_list"))


    def get(self, request, course_id):
        course = get_object_or_404(Course, course_id=course_id)
        return render(request, "dashboard-course-form.html", {
            "course": course,
            "programs": Program.objects.all(),
            "mode": "update"
        })


    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'

    def post(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowd to delete courses.")
        
        courses = request.POST.get('selected-courses-delete', '').strip()

        if courses == "" or courses is None:
            return redirect(reverse_lazy('dashboard_course_list'))

        courses_selected = courses.split(',')

        for id in courses_selected:
            status = delete_course(id)

            if not status["success"]:
                messages.error(request, status["error"])
                return redirect(reverse_lazy('dashboard_course_list'))

        if (len(courses_selected) > 4):
            messages.success(request, f"Courses {", ".join(courses_selected[:4])}, and {len(courses_selected) - 4} others deleted successfully!")
        elif (len(courses_selected) == 1):
            messages.success(request, f"Course {courses_selected[0]} deleted successfully!")
        else:
            messages.success(request, f"Courses {", ".join(courses_selected)} deleted successfully!")

        return redirect(reverse_lazy('dashboard_course_list'))
    

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser