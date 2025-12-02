from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment
from users.models import CustomUser
from teacher.models import TeacherProfile
from .forms import CourseForm, LessonForm  # If you have forms.py for instructor use

# List all courses (visible to everyone)
def course_list(request):
    courses = Course.objects.all().order_by('-created_on')
    return render(request, 'courses/course_list.html', {'courses': courses})

# Course detail with list of lessons
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled
    })

# Enroll a student in a course
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"You have enrolled in {course.title}.")
    return redirect('courses:all_courses')

# View enrolled courses for a student
@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})

# Instructor-only: Create new course
@login_required
def create_course(request):
    try:
        # Confirm user has a TeacherProfile
        teacher_profile = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        messages.error(request, "You must complete your teacher profile before creating a course.")
        return redirect('teacher:edit_profile')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = teacher_profile  # ✅ Assign the user, not the profile
            course.save()
            messages.success(request, "Course created successfully.")
            return redirect('courses:course_list')  # ✅ Redirect only on success
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})


# Instructor-only: View courses created by them
@login_required
def instructor_courses(request):
    try:
        teacher = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        messages.error(request, "Only teachers can view their courses.")
        return redirect('course_list')

    courses = Course.objects.filter(instructor=teacher)
    return render(request, 'courses/instructor_courses.html', {'courses': courses})

# Instructor-only: Add lesson to a course
@login_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.instructor.user != request.user:
        messages.error(request, "You are not allowed to add lessons to this course.")
        return redirect('instructor_courses')

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, "Lesson added successfully.")
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = LessonForm()
    return render(request, 'courses/add_lesson.html', {'form': form, 'course': course})

# View specific lesson content (only if enrolled)
@login_required
def view_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course

    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    if not is_enrolled and request.user != course.instructor.user:
        messages.error(request, "Access denied. Please enroll to view this lesson.")
        return redirect('course_detail', course_id=course.id)

    return render(request, 'courses/view_lesson.html', {'lesson': lesson})

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})

# courses/views.py


@login_required
def all_courses(request):
    courses = Course.objects.all()
    # Get all Enrollment objects for this user
    user_enrollments = Enrollment.objects.filter(student=request.user)
    # Extract the courses
    enrolled_courses = [en.course for en in user_enrollments]

    return render(request, 'courses/all_courses.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
    })

