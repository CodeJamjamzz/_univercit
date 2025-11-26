from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from curriculum.models import Program
from .models import Student

# Create your views here.
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'student_detail.html', {'student': student})

def student_edit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        program_id = request.POST.get('programId')
        student.programId = Program.objects.get(pk=program_id) if program_id else None
        student.fname = request.POST.get('fname')
        student.lname = request.POST.get('lname')
        student.username = request.POST.get('username')
        student.email = request.POST.get('email')
        student.password = request.POST.get('password')
        student.save()
        return redirect('student_list')

    programs = Program.objects.all()
    return render(request, 'student_form.html', {'student': student, 'programs': programs})

def student_delete(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})


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
        return render(request, self.template)
    def post(self, request):
        program_code = request.POST['program']
        program = Program.objects.get(program_code=program_code)

        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirm_password']
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

class HomeView(View):

    template = "index.html"
    def get(self, request):
        print("hello world")
        return render(request, self.template)