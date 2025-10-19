from django.db import models

from curriculum.models import Course
from user.models import Student

# Create your models here.
class Forum(models.Model):
    # Primary Key
    forum_id = models.AutoField(primary_key=True)
    # Attributes
    forum_title = models.TextField()
    forum_desc = models.TextField()
    # Foreign Key(s)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def get_threads(self):
        return Thread.objects.filter(forum_id=self.forum_id)

class Thread(models.Model):
    # Primary Key
    thread_id = models.AutoField(primary_key=True)
    # Attributes
    thread_title = models.TextField()
    date_created = models.DateTimeField()
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    # Foreign Key(s)
    forum_id = models.ForeignKey(Forum, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)

    def get_comments(self):
        return Comment.objects.filter(thread_id=self.thread_id)

class Comment(models.Model):
    # Primary Key
    comment_id = models.AutoField(primary_key=True)
    # Attributes
    content = models.TextField()
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    # Foreign Key(s)
    thread_id = models.ForeignKey(Thread, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
