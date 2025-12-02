from django.db import models

# Create your models here.
# courses/models.py
from django.db import models
from teacher.models import TeacherProfile
from users.models import CustomUser


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    duration_weeks = models.PositiveIntegerField()
    course_file = models.FileField(upload_to='course_files/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video = models.FileField(upload_to='lesson_videos/', null=True, blank=True)

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_on = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ('student', 'course')
