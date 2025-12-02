from django.shortcuts import render

# Create your views here.
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from student.models import StudentProfile
from .forms import StudentRegisterForm, TeacherRegisterForm
from .models import CustomUser


def home(request):
    return render(request, 'users/home.html')


from student.models import StudentProfile


def student_register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Option 1: Auto-generate enrollment number
            enrollment_number = f"ENR{user.id:05d}"

            # Create StudentProfile
            StudentProfile.objects.create(
                user=user,
                enrollment_number=enrollment_number
            )

            login(request, user)
            messages.success(request, "Student registered successfully!")
            return redirect('student:student_dashboard')
    else:
        form = StudentRegisterForm()
    return render(request, 'users/student_register.html', {'form': form})


def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Teacher registered successfully!")
            return redirect('teacher:teacher_dashboard')  # or appropriate view
    else:
        form = TeacherRegisterForm()
    return render(request, 'users/teacher_register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('route_by_role')  # redirect based on role
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect('home')


@login_required
def route_by_role(request):
    user = request.user
    if user.is_superuser or user.is_adminuser:
        return redirect('admin_dashboard')
    elif user.is_teacher:
        return redirect('teacher:teacher_dashboard')
    elif user.is_student:
        return redirect('student:student_dashboard')
    else:
        return redirect('home')
