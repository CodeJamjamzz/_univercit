from django.shortcuts import render
from django.views import View
from curriculum.models import Program
from .models import Student

# Create your views here.
class LoginView(View):
    template = "login.html"
    def get(self, request):
        return render(request, self.template)

    def login_student(self, request):
        if(request.method == "POST"):
            email = request.POST["email"]
            password = request.POST["password"]

            try:
                Student.objects.get(email = email, password = password)
                # return redirect("dashboard.html") // redirect after login
            except Student.DoesNotExist:
                return render(request, self.template, {'error': 'user does not exist'})

class SignInView(View):
    template = "signin.html"
    def get(self, request):
        return render(request, self.template)
    def signin_student(self, request):
        if(request.method == "POST"):
            program = Program.objects.get(program_desc= "BSCS")
            programId = program.id
            fname = request.POST['fname']
            lname = request.POST['lname']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            Student.objects.create(
                program_id=programId,
                fname=fname,
                lname=lname,
                username=username,
                email=email,
                password=password
            )
            # return redirect("dashboard.html") // dashboard template
        return render(request, self.template)

class HomeView(View):
    template = "home.html"
    def get(self, request):
        return render(request, self.template)