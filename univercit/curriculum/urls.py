from django.urls import path
from . import views

# Create your tests here.
urlpatterns = [
    # Programs
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/<str:program_code>/', views.ProgramDetailView.as_view(), name='program_detail'),

    # Courses
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<str:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),

    # Dashboard
    path('dashboard/programs/', views.DashboardProgramListView.as_view(), name='dashboard_program_list'),
    path('dashboard/programs/create/', views.ProgramCreateView.as_view(), name='dashboard_program_create'),
    path('dashboard/programs/<str:program_code>/update/', views.ProgramUpdateView.as_view(), name='dashboard_program_update'),
    path('dashboard/programs/delete/', views.ProgramDeleteView.as_view(), name='dashboard_program_delete'),

    path('dashboard/courses/', views.DashboardCourseListView.as_view(), name='dashboard_course_list'),
    path('dashboard/courses/create/', views.CourseCreateView.as_view(), name='dashboard_course_create'),
    path('dashboard/courses/<str:course_id>/update/', views.CourseUpdateView.as_view(), name='dashboard_course_update'),
    path('dashboard/courses/delete/', views.CourseDeleteView.as_view(), name='dashboard_course_delete'),
]
