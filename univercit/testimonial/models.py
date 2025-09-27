from django.db import models

# Create your models here.
class Testimonial(models.Model):
    testimonial_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('curriculum.Course', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name