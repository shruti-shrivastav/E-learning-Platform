from django.shortcuts import render

# Create your views here.
# teacher/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TeacherProfile
from .forms import TeacherProfileForm  # Make sure you create this form
from courses.models import Course

# View teacher profile (only for logged-in teachers)
@login_required
def teacher_profile(request):
    try:
        profile = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('home')  # Redirect to homepage or dashboard

    return render(request, 'teacher/profile.html', {'profile': profile})

# Edit teacher profile
@login_required
def edit_profile(request):
    try:
        profile = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        profile = TeacherProfile(user=request.user)  # Create new if not exist

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('teacher:teacher_dashboard')
    else:
        form = TeacherProfileForm(instance=profile)

    return render(request, 'teacher/edit_profile.html', {'form': form})

# View all courses created by the teacher
@login_required
def my_courses(request):
    try:
        teacher = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        messages.error(request, "You must be a teacher to view your courses.")
        return redirect('home')

    courses = Course.objects.filter(instructor=teacher)
    return render(request, 'teacher/my_courses.html', {'courses': courses})

@login_required
def teacher_dashboard(request):
    teacher = request.user

    # Try to fetch the associated TeacherProfile
    try:
        teacher_profile = teacher.teacherprofile
    except TeacherProfile.DoesNotExist:
        teacher_profile = None

    # Fetch courses created by this teacher
    courses = Course.objects.filter(instructor=teacher_profile)

    return render(request, 'teacher/dashboard.html', {
        'teacher': teacher,
        'profile': teacher_profile,
        'courses': courses,
    })