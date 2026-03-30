from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import TeacherClass


@login_required
def teacher_dashboard(request):
    if request.user.role != "teacher":
        messages.error(request, "You are not allowed to access the teacher dashboard.")
        return redirect("login")

    today_classes = request.user.assigned_classes.all()[:5]

    context = {
        "today_classes": today_classes,
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
