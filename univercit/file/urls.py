from django.urls import path
from . import views

urlpatterns = [
    # placeholder
    path('fileview/', views.FileView.as_view(), name='fileView'),
    # where other apps will send data
    path('submit/', views.submit, name='submit'),
]
