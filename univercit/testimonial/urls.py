from django.urls import path
from . import views

urlpatterns = [
    # placeholder
    path('testimonialview/', views.TestimonialView.as_view(), name='testimonialView'),
    # where other apps will send data
    path('submit/', views.submit, name='submit'),
]
