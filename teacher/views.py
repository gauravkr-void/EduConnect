from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

<<<<<<< HEAD
from .forms import AddStudentToClassForm, TeacherClassForm, TeacherProfileUpdateForm
from .models import StudentClassMembership, TeacherClass


def _teacher_required(request):
    if request.user.role != "teacher":
        messages.error(request, "You are not allowed to access this page.")
        return False
    return True

=======
from .forms import TeacherProfileUpdateForm
from .models import TeacherClass
# Karan's Addition: Importing Subject model
from accounts.models import Subject
from accounts.utils import generate_attendance_qr 
>>>>>>> 237c3ec7b9c4ac0db7f364399a5e1ec6901a1d98

@login_required
def teacher_dashboard(request):
    if not _teacher_required(request):
        return redirect("login")

<<<<<<< HEAD
    today_classes = request.user.assigned_classes.prefetch_related("student_memberships")[:5]
    total_classes = request.user.assigned_classes.count()
    total_students = StudentClassMembership.objects.filter(classroom__teacher=request.user).values("student").distinct().count()
=======
    # Backend 1's logic
    today_classes = request.user.assigned_classes.all()[:5]
>>>>>>> 237c3ec7b9c4ac0db7f364399a5e1ec6901a1d98

    # Karan's Addition: Fetching subjects for the QR buttons
    subjects = Subject.objects.filter(teacher=request.user)

    context = {
        "today_classes": today_classes,
<<<<<<< HEAD
        "total_classes": total_classes,
        "total_students": total_students,
=======
        "subjects": subjects, # Passing subjects to the template
>>>>>>> 237c3ec7b9c4ac0db7f364399a5e1ec6901a1d98
    }
    return render(request, "teacher/teacher_dashboard.html", context)


@login_required
def teacher_class_view(request):
    if not _teacher_required(request):
        return redirect("login")

    if request.method == "POST":
        form = TeacherClassForm(request.POST)
        if form.is_valid():
            teacher_class = form.save(commit=False)
            teacher_class.teacher = request.user
            teacher_class.save()
            messages.success(request, "Class created successfully.")
            return redirect("teacher_class_detail", class_id=teacher_class.id)
    else:
        form = TeacherClassForm()

    teacher_classes = (
        TeacherClass.objects.filter(teacher=request.user)
        .prefetch_related("student_memberships__student")
    )

    context = {
        "form": form,
        "teacher_classes": teacher_classes,
    }
    return render(request, "teacher/teacher_class.html", context)


@login_required
def teacher_class_detail(request, class_id):
    if not _teacher_required(request):
        return redirect("login")

    classroom = get_object_or_404(
        TeacherClass.objects.prefetch_related("student_memberships__student"),
        id=class_id,
        teacher=request.user,
    )

    if request.method == "POST":
        form = AddStudentToClassForm(request.POST, classroom=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added to class.")
            return redirect("teacher_class_detail", class_id=classroom.id)
    else:
        form = AddStudentToClassForm(classroom=classroom)

    memberships = classroom.student_memberships.select_related("student").order_by("student__full_name", "student__email")

    context = {
        "classroom": classroom,
        "form": form,
        "has_available_students": form.fields["student"].queryset.exists(),
        "memberships": memberships,
    }
    return render(request, "teacher/teacher_class_detail.html", context)


@login_required
def teacher_class_edit(request, class_id):
    if not _teacher_required(request):
        return redirect("login")

    classroom = get_object_or_404(TeacherClass, id=class_id, teacher=request.user)

    if request.method == "POST":
        form = TeacherClassForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Class details updated.")
            return redirect("teacher_class_detail", class_id=classroom.id)
    else:
        form = TeacherClassForm(instance=classroom)

    return render(request, "teacher/teacher_class_form.html", {"form": form, "classroom": classroom})


@login_required
def teacher_class_remove_student(request, class_id, membership_id):
    if not _teacher_required(request):
        return redirect("login")

    classroom = get_object_or_404(TeacherClass, id=class_id, teacher=request.user)
    membership = get_object_or_404(StudentClassMembership, id=membership_id, classroom=classroom)

    if request.method == "POST":
        student_name = membership.student.full_name
        membership.delete()
        messages.success(request, f"{student_name} removed from {classroom.name}.")

    return redirect("teacher_class_detail", class_id=classroom.id)


@login_required
def teacher_profile_update(request):
    if not _teacher_required(request):
        return redirect("login")

    if request.method == "POST":
        form = TeacherProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("teacher_dashboard")
    else:
        form = TeacherProfileUpdateForm(instance=request.user)

    return render(request, "teacher/teacher_profile_update.html", {"form": form})

# --- Karan's Work: QR Generation Logic (Appended) ---

@login_required
def generate_qr_view(request, subject_id):
    if request.user.role == 'teacher':
        try:
            subject = Subject.objects.get(id=subject_id, teacher=request.user)
            # QR generate karna
            qr_url = generate_attendance_qr(request.user.id, subject.id)
            
            context = {
                'qr_url': qr_url,
                'subject': subject,
            }
            return render(request, 'teacher/display_qr.html', context)
        except Subject.DoesNotExist:
            messages.error(request, "Subject not found.")
            return redirect("teacher_dashboard")
    else:
        return redirect("login")