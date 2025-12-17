from .import views
from django.urls import path

urlpatterns = [
    # where other apps will send data
    path('rate/submit/', views.rate, name='rate'),
]