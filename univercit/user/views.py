from django.shortcuts import render, redirect
from django.views import View
from curriculum.models import Program
from .models import Student

# Create your views here.
class LogInView(View):
    template = "login.html"
    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            Student.objects.get(email = email, password = password)
            return redirect("home") # redirect after login
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
        return redirect('home')

class HomeView(View):
    template = "home.html"
    def get(self, request):
        return render(request, self.template)