from django.urls import path
from . import views
from .views import delete_student

urlpatterns = [
    path('signin/', views.SignInView.as_view(), name="signin"),
    path('login/', views.LogInView.as_view(), name="login"),
    path('logout/', views.logout_view, name="student_logout"),
    path('', views.index, name="index"),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/updateform/<int:id>/', views.TableView.as_view(), name='update_student'),
    path('dashboard/delete/<int:id>/', delete_student, name='delete_student'),
]