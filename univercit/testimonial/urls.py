from django.urls import path
from . import views

urlpatterns = [
    # placeholder
    path('testimonialview/', views.TestimonialView.as_view(), name='testimonialView'),
    path('submit/', views.submit, name='submit'),
    path('list/', views.testimonial_list, name='testimonial_list'),
]

from django.urls import path
from . import views

urlpatterns = [
    # placeholder
    path('testimonialview/', views.TestimonialView.as_view(), name='testimonialView'),
    path('submit/', views.submit, name='submit'),
    path('list/', views.testimonial_list, name='testimonial_list'),
    path('write/', views.testimonial_write_form, name='testimonial_write_form'),
    path('delete/<int:testimonial_id>/', views.delete_testimonial, name='delete_testimonial'),
    path('edit/<int:testimonial_id>/', views.edit_testimonial, name='edit_testimonial'),
]
