from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('courses/', views.my_courses, name='my_courses'),

    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]
