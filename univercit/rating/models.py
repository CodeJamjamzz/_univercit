from django.db import models

from user.models import Student
from discussion.models import Comment
from file.models import File
from discussion.models import Thread


# Create your models here.
class Rating(models.Model):
    ratingId = models.AutoField(primary_key=True)
    isUpvoted = models.BooleanField(default=False)
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)

class CommentRating(Rating):
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    pass
class FileRating(Rating):
    fileId = models.ForeignKey(File, on_delete=models.CASCADE)
    pass
class ThreadRating(Rating):
    threadId = models.ForeignKey(Thread, on_delete=models.CASCADE)
    pass