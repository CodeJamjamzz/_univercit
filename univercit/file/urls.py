from django.urls import path
from . import views

urlpatterns = [
    # placeholder
    path('fileview/', views.FileView.as_view(), name='fileView'),
    path('submit/', views.submit, name='submit'),
]

from django.urls import path
from . import views

urlpatterns = [
    # placeholder
    path('fileview/', views.FileView.as_view(), name='fileView'),
    path('submit/', views.submit, name='submit'),
    path('uploadform/', views.file_upload_form, name='file_upload_form'),
]

