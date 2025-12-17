from django.db import models
from curriculum.models import Program


# Create your models here.
class Student(models.Model):
    studentId = models.AutoField(primary_key=True)
    programId = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"""id: {self.studentId}
        Firstname: {self.fname}
        Lastname: {self.lname}
        Username: {self.username}
        Email: {self.email}
        """

    @property
    def id(self):
        return self.studentId

