from django.urls import path
from . import views

# Create your tests here.
urlpatterns = [
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/<str:program_code>/', views.ProgramDetailView.as_view(), name='program_detail'),
    # path('programs/<str:program_code>/<str:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),

    # path('programs/create/', views.ProgramCreateView.as_view(), name='program_create'),
    # path('programs/<str:program_code>/update/', views.ProgramUpdateView.as_view(), name='program_update'),
    # path('programs/<str:program_code>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),

    # Courses
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<str:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    # path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    # path('courses/<str:course_id>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    # path('courses/<str:course_id>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # Program–Course Relationship
    # path('programs/<str:program_code>/courses/', views.ProgramCoursesView.as_view(), name='program_courses'),
    # path('programs/<str:program_code>/add-course/<str:course_id', views.ProgramCoursesAddView.as_view(), name='add_course_to_program'),
    # path('programs/<str:program_code>/remove-course/<str:course_id>/', views.ProgramCoursesDeleteView.as_view(), name='remove_course_from_program'),

    path('dashboard/programs/', views.DashboardProgramListView.as_view(), name='dashboard_program_list'),
    path('dashboard/programs/create/', views.ProgramCreateView.as_view(), name='dashboard_program_create'),
    path('dashboard/programs/<str:program_code>/update/', views.ProgramUpdateView.as_view(), name='dashboard_program_update'),
    path('dashboard/courses/', views.DashboardCourseListView.as_view(), name='dashboard_course_list'),
    path('dashboard/courses/create/', views.CourseCreateView.as_view(), name='dashboard_course_create'),
    path('dashboard/courses/<str:course_id>/update/', views.CourseUpdateView.as_view(), name='dashboard_course_update')
]