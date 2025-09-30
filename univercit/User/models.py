from django.db import models
# Create your models here.
class Student(models.Model):
    studentId = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"""id: {self.student_id}
        Firstname: {self.fname}
        Lastname: {self.lname}
        Username: {self.username}
        Email: {self.email}
        """

