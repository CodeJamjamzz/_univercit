from django.db import models

from user.models import Student

from curriculum.models import Course


# Create your models here.
class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    file_url = models.FileField(upload_to='files/')
    file_desc = models.TextField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.file_name
    
    