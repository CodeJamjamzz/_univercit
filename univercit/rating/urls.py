from .import views
from django.urls import path

urlpatterns = [
    # placeholder
    path('ratingview/', views.RatingView.as_view(), name='ratingView'),
    # where other apps will send data
    path('rate/submit/', views.rate, name='rate'),
]