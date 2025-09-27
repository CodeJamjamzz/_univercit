from django.contrib import admin

from rating.models import Rating, CommentRating, ThreadRating, FileRating

# Register your models here.
admin.site.register(Rating)
admin.site.register(CommentRating)
admin.site.register(FileRating)
admin.site.register(ThreadRating)