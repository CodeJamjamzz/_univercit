from .import views
from django.urls import path

urlpatterns = [
    path('rating/', views.RatingView.as_view(), name='login'),
]