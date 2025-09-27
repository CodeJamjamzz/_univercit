from django.db import models

# Create your models here.
class Rating(models.Model):
    ratingID = models.AutoField(primary_key=True)
    isUpvoted = models.BooleanField(default=False)

class CommentRating(Rating):
    pass
class FileRating(Rating):
    pass
class ThreadRating(Rating):
    pass