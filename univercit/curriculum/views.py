# curriculum/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.db.models import Q

from .models import Program, Course
from .utils import *

# Program Views

# Limit the program the can be seen by the User on what program they are in
class ProgramListView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        query = request.GET.get('query', '')
        if query:
            query = query.strip()
            programs = Program.objects.filter(
                Q(program_code__icontains=query) | Q(program_desc__icontains=query)
            )
        else:
            programs = Program.objects.all()

        return render(request, "all-programs.html", {
            "programs": programs
        })
    
class DashboardProgramListView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        programs = Program.objects.all()

        return render(request, "dashboard-programs.html", {
            "programs": programs
        })


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


class ProgramCreateView(LoginRequiredMixin, View):
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
            })

        program = Program.objects.create(
            program_code=program_code,
            program_name=program_name,
            program_desc=program_desc
        )

        if program_courses is not None and program_courses != "":
            for id in program_courses.split(","):
                course = get_object_or_404(Course, course_id=id)
                program.courses.add(course)

        messages.success(request, f"Program {program_code} created successfully!")
        if action == "create":
            return redirect(reverse_lazy("dashboard_program_list"))
        elif action == "create-add":
            return redirect(reverse_lazy("dashboard_program_create"))
        
    
    def get(self, request):
        return render(request, 'dashboard-program-form.html', {
            "courses": Course.objects.all(),
            "mode": "create"
        })


class ProgramUpdateView(LoginRequiredMixin, View):
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

        program.program_name=program_name
        program.program_desc=program_desc
        program.save()

        if program_courses is not None and program_courses != "":
            course_id = [id.strip() for id in program_courses.split(",")]
            courses = Course.objects.filter(course_id__in=course_id)
            program.courses.set(courses)
        else:
            program.courses.clear()

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

    

class ProgramDeleteView(LoginRequiredMixin, View):    
    login_url = '/login/'

    def post(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowd to delete programs.")
        
        programs = request.POST.get('selected-programs-delete', '').strip()

        if programs == "" or programs is None:
            return redirect(reverse_lazy('dashboard_program_list'))
        
        programs_selected = programs.split(',')

        for code in programs_selected:
            program = get_object_or_404(Program, program_code=code)
            program.delete()

        if (len(programs_selected) > 4):
            messages.success(request, f"Programs {", ".join(programs_selected[:4])}, and {len(programs_selected) - 4} others deleted successfully!")
        elif (len(programs_selected) == 1):
            messages.success(request, f"Program {programs_selected[0]} deleted successfully!")
        else:
            messages.success(request, f"Programs {", ".join(programs_selected)} deleted successfully!")

        return redirect(reverse_lazy('dashboard_program_list'))


# Course Views
class CourseListView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        query = request.GET.get('query', '')

        with connection.cursor() as cursor:
            courses = get_courses(query)

            for course in courses:
                programs = get_courses_programs(course["course_id"])
                course["programs"] = programs
            
            print(courses)
                
            return render(request, "all-courses.html", {
                "courses": courses,
            })


class DashboardCourseListView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        courses = Course.objects.all()

        return render(request, "dashboard-courses.html", {
            "courses": courses
        })
    

class CourseDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    
    def get(self, request, course_id):
        course = get_object_or_404(Course, course_id=course_id)
        return render(request, 'course.html', {
            "programs": course.programs,
            "course": course
        })


class CourseCreateView(LoginRequiredMixin, View):
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
        
        course = Course.objects.create(
            course_id=course_id,
            course_name=course_name,
            course_desc=course_desc
        )

        if course_programs is not None and course_programs != "":
            for code in course_programs.split(","):
                program = get_object_or_404(Program, program_code=code)
                course.programs.add(program)

        messages.success(request, f"Course {course_id} created successfully!")
        if action == "create":
            return redirect(reverse_lazy("dashboard_course_list"))
        elif action == "create-add":
            return redirect(reverse_lazy("dashboard_course_create"))
        
        return redirect(reverse_lazy("dashboard_course_list"))
    

    def get(self, request):
        return render(request, "dashboard-course-form.html", {
            "programs": Program.objects.all(),
            "mode": "create",
        })
    

class CourseUpdateView(LoginRequiredMixin, View):
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
        
        course.course_name = course_name
        course.course_desc = course_desc
        course.save()
             
        if course_programs is not None and course_programs != "":
            program_codes = [code.strip() for code in course_programs.split(",")]
            programs = Program.objects.filter(program_code__in=program_codes)
            course.programs.set(programs) 
        else:
            course.programs.clear() 

        messages.success(request, f"Course {course_id} updated successfully!")
        if action == "create":
            return redirect(reverse_lazy("dashboard_course_list"))
        elif action == "save-edit":
            return redirect(reverse_lazy("dashboard_course_update", args=(course_id,)))

    
    def get(self, request, course_id):
        course = get_object_or_404(Course, course_id=course_id)
        return render(request, "dashboard-course-form.html", {
            "course": course,
            "programs": Program.objects.all(),
            "mode": "update"
        })


class CourseDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowd to delete courses.")
        
        courses = request.POST.get('selected-courses-delete', '').strip()

        if courses == "" or courses is None:
            return redirect(reverse_lazy('dashboard_course_list'))

        courses_selected = courses.split(',')    

        for id in courses_selected:
            course = get_object_or_404(Course, course_id=id)
            course.delete()

        if (len(courses_selected) > 4):
            messages.success(request, f"Courses {", ".join(courses_selected[:4])}, and {len(courses_selected) - 4} others deleted successfully!")
        elif (len(courses_selected) == 1):
            messages.success(request, f"Course {courses_selected[0]} deleted successfully!")
        else:
            messages.success(request, f"Courses {", ".join(courses_selected)} deleted successfully!")

        return redirect(reverse_lazy('dashboard_course_list'))


# Relationship Views
class ProgramCoursesView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'program_courses.html'

    def get(self, request, program_code):
        program = get_object_or_404(Program, program_code=program_code)
        courses = program.courses.all()
        return render(request, "program_courses.html", {
            "program": program,
            "courses": courses
        })


class ProgramCoursesAddView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, program_code, course_id):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to modify programs and courses in this program.")

        program = get_object_or_404(Program, program_code=program_code)
        course = get_object_or_404(Course, course_id=course_id)
        program.courses.add(course)

        return redirect('program_courses', program_code=program.program_code)
    

class ProgramCoursesDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, program_code, course_id):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to modify programs and courses in this program.")

        program = get_object_or_404(Program, program_code=program_code)
        course = get_object_or_404(Course, course_id=course_id)
        program.courses.remove(course)

        return redirect('program_courses', program_code=program.program_code)