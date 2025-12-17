from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignInView.as_view(), name="signin"),
    path('login/', views.LogInView.as_view(), name="login"),
    path('', views.index, name="index"),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]