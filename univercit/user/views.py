from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Student
from curriculum.models import Program

# Create your views here.
def index(request):
    return render(request, 'index.html')

def student_list(request):
    students = list(Student.objects.values())
    return JsonResponse({'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return JsonResponse({
        'studentId': student.studentId,
        'programId': student.programId_id,
        'fname': student.fname,
        'lname': student.lname,
        'username': student.username,
        'email': student.email,
        'password': student.password
    })

def student_edit(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=student_id)
        program_id = request.POST.get('programId')
        student.programId_id = program_id if program_id else None
        student.fname = request.POST.get('fname')
        student.lname = request.POST.get('lname')
        student.username = request.POST.get('username')
        student.email = request.POST.get('email')
        student.password = request.POST.get('password')
        student.save()
        return HttpResponse("Student updated successfully.")
    return HttpResponse("Use POST method to edit student.")

def student_delete(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=student_id)
        student.delete()
        return HttpResponse("Student deleted successfully.")
    return HttpResponse("Use POST method to delete student.")


class LogInView(View):
    template = "login.html"
    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            Student.objects.get(email = email, password = password)
            return redirect("index") # redirect after login
        except Student.DoesNotExist:
            return render(request, self.template, {'error': 'user does not exist'})

class SignInView(View):
    template = "signin.html"

    def get(self, request):
        programs = Program.objects.all()
        return render(request, self.template, {'programs': programs})
    def post(self, request):
        program_code = request.POST.get("programId")
        program = Program.objects.get(program_code=program_code)
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirm_password')

        if confirmpassword != password:
            return render(request, self.template, {'error': 'confirm password incorrect'})

        Student.objects.create(
            programId=program,
            fname=firstname,
            lname=lastname,
            username=username,
            email=email,
            password=password
        )

        return redirect('index')

# class HomeView(View):

#     template = "index.html"
#     def get(self, request):
#         print("hello world")
#         return render(request, self.template)
