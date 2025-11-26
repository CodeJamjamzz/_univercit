from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignInView.as_view(), name="signin"),
    path('login/', views.LogInView.as_view(), name="login"),
    # path('', views.HomeView.as_view(), name="index"),
    path('', views.index, name="index"),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/<int:student_id>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student_delete'),
]