from django.db import models

# Create your models here.
class Program(models.Model):
    program_code = models.CharField(max_length=10, primary_key=True)
    program_desc = models.TextField()
    courses = models.ManyToManyField('Course', related_name="programs")


class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    course_name = models.CharField(max_length=50)
    course_desc = models.TextField()