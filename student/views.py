from django.shortcuts import render

# Create your views here.
# student/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import StudentProfile, Enrollment
from users.models import CustomUser
from django.contrib import messages

# View: Student Dashboard
@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('home')  # Only students allowed

    profile = get_object_or_404(StudentProfile, user=request.user)
    enrollments = Enrollment.objects.filter(student=profile)
    enrolled_courses = [enroll.course for enroll in enrollments]

    return render(request, 'student/dashboard.html', {
        'profile': profile,
        'enrolled_courses': enrolled_courses
    })

# View: All Available Courses for Enrollment
@login_required
def available_courses(request):
    if not request.user.is_student:
        return redirect('home')

    profile = get_object_or_404(StudentProfile, user=request.user)
    enrolled_courses = Enrollment.objects.filter(student=profile).values_list('course_id', flat=True)
    courses = Course.objects.exclude(id__in=enrolled_courses)

    return render(request, 'student/available_courses.html', {
        'courses': courses
    })

# View: Enroll in a Course
@login_required
def enroll_in_course(request, course_id):
    if not request.user.is_student:
        return redirect('home')

    profile = get_object_or_404(StudentProfile, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    # Prevent duplicate enrollments
    if Enrollment.objects.filter(student=profile, course=course).exists():
        messages.warning(request, "You are already enrolled in this course.")
    else:
        Enrollment.objects.create(student=profile, course=course)
        messages.success(request, f"Enrolled in {course.title} successfully.")

    return redirect('student_dashboard')

# View: Profile Page
@login_required
def student_profile(request):
    if not request.user.is_student:
        return redirect('home')

    profile = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'student/profile.html', {'profile': profile})

