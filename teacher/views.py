from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import TeacherProfileUpdateForm
from .models import TeacherClass
# Karan's Addition: Importing Subject model
from accounts.models import Subject
from accounts.utils import generate_attendance_qr 

@login_required
def teacher_dashboard(request):
    if request.user.role != "teacher":
        messages.error(request, "You are not allowed to access the teacher dashboard.")
        return redirect("login")

    # Backend 1's logic
    today_classes = request.user.assigned_classes.all()[:5]

    # Karan's Addition: Fetching subjects for the QR buttons
    subjects = Subject.objects.filter(teacher=request.user)

    context = {
        "today_classes": today_classes,
        "subjects": subjects, # Passing subjects to the template
    }
    return render(request, "teacher/teacher_dashboard.html", context)


@login_required
def teacher_class_view(request):
    if request.user.role != "teacher":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")

    teacher_classes = (
        TeacherClass.objects.filter(teacher=request.user)
        .prefetch_related("student_memberships__student")
    )

    context = {
        "teacher_classes": teacher_classes,
    }
    return render(request, "teacher/teacher_class.html", context)


@login_required
def teacher_profile_update(request):
    if request.user.role != "teacher":
        messages.error(request, "You are not allowed to access this page.")
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