# student/urls.py
from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('courses/', views.available_courses, name='available_courses'),
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_course'),
]
