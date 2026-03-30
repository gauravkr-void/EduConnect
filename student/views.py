from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from teacher.models import StudentClassMembership


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access the student dashboard.")
        return redirect("login")

    memberships = (
        StudentClassMembership.objects
        .filter(student=request.user)
        .select_related("classroom", "classroom__teacher")
    )

    enrolled_courses = [membership.classroom for membership in memberships]
    today_schedule = enrolled_courses[:5]

    context = {
        "enrolled_courses": enrolled_courses,
        "today_schedule": today_schedule,
    }
    return render(request, "student/student_dashboard.html", context)


@login_required
def student_performance(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")
    return render(request, "student/student_performance.html")


@login_required
def student_queries(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")
    return render(request, "student/student_queries.html")


@login_required
def student_messages(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")
    return render(request, "student/student_messages.html")


@login_required
def student_attendance(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")
    return render(request, "student/student_attendance.html")


@login_required
def student_announcements(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")
    return render(request, "student/student_announcements.html")


@login_required
def student_qr_attendance(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")
    return render(request, "student/student_qr_attendance.html")
