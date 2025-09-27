from django.db import models

# Create your models here.
class Forum(models.Model):
    # Primary Key
    forumId = models.AutoField(primary_key=True)
    # Attributes
    forumTitle = models.TextField()
    forumDesc = models.TextField()
    # Foreign Key(s)
    # courseId FK

class Thread(models.Model):
    # Primary Key
    threadId = models.AutoField(primary_key=True)
    # Attributes
    threadTitle = models.TextField()
    dateCreated = models.DateTimeField()
    upvoteCount = models.IntegerField(default=0)
    downvoteCount = models.IntegerField(default=0)
    isVisible = models.BooleanField(default=True)
    # Foreign Key(s)
    forumId = models.ForeignKey(Forum, on_delete=models.CASCADE)

class Comment(models.Model):
    # Primary Key
    commentId = models.AutoField(primary_key=True)
    # Attributes
    content = models.TextField()
    upvoteCount = models.IntegerField(default=0)
    downvoteCount = models.IntegerField(default=0)
    isVisible = models.BooleanField(default=True)
    # Foreign Key(s)
    threadId = models.ForeignKey(Thread, on_delete=models.CASCADE)
    # studentId FK
