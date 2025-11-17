# curriculum/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Program, Course
from django.http import HttpResponseForbidden
from django.db.models import Q


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

        return render(request, "all_programs.html", {
            "programs": programs
        })


class ProgramDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, program_code):
        program = get_object_or_404(Program, pk=program_code)
        return render(request, 'program.html', {
            "program": program
        })


class ProgramCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to create programs.")
        
        program_code = request.POST.get('program_code')
        program_desc = request.POST.get('program_desc')

        if program_code and program_desc:
            Program.objects.create(
                program_code=program_code,
                program_desc=program_desc
            )
            return redirect(reverse_lazy('program_list'))

        return HttpResponseForbidden("Missing program data.")


class ProgramUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def post(self, request, program_code):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to update programs.")
        
        program = get_object_or_404(Program, program_code=program_code)
        new_desc = request.POST.get('program_desc')

        if new_desc:
            program.program_desc = new_desc
            program.save()
            return redirect(reverse_lazy('program_list'))
        
        return HttpResponseForbidden("Missing program description.")

    

class ProgramDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, program_code):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowd to delete programs.")
        
        program = get_object_or_404(Program, program_code=program_code)
        program.delete()
        return redirect(reverse_lazy('program_list'))


# Course Views
class CourseListView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        query = request.GET.get('query', '')
        if query:
            query = query.strip()
            courses = Course.objects.filter(
                Q(course_id__icontains=query) | Q(course_name__icontains=query)
            )
        else:
            courses = Course.objects.all()

        return render(request, "all_courses.html", {
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
    model = Course
    fields = ['courseId', 'courseName', 'courseDesc']
    success_url = reverse_lazy('course_list')
    login_url = '/login/'

    def post(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to create courses.")
        
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        course_desc = request.POST.get('ccourse_desc')

        if course_id and course_name and course_desc:
            Course.objects.create(
                course_id=course_id,
                course_name=course_name,
                course_desc=course_desc
            )
            return redirect(reverse_lazy('course_list'))

        return HttpResponseForbidden("Missing course data.")


class CourseUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, course_id):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to update courses.")
        
        course = get_object_or_404(Course, course_id=course_id)
        new_desc = request.POST.get('course_desc')

        if new_desc:
            course.course_desc = new_desc
            course.save()
            return redirect(reverse_lazy('course_list'))
            
        return HttpResponseForbidden("Missing course description.")


class CourseDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, course_id):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowd to delete courses.")
        
        course = get_object_or_404(Course, course_code=course_id)
        course.delete()
        return redirect(reverse_lazy('course_list'))


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