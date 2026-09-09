from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render
<<<<<<< HEAD
from django.utils import timezone

from teacher.models import StudentClassMembership
from .forms import StudentMessageForm, StudentProfileUpdateForm, StudentQueryForm
from .models import Announcement, Attendance, Course, Message, Performance, Query


def _student_classrooms(user):
    return (
        StudentClassMembership.objects
        .filter(student=user)
        .select_related("classroom", "classroom__teacher")
    )


def _student_classroom_ids(user):
    return _student_classrooms(user).values_list("classroom_id", flat=True)

=======
from django.http import JsonResponse # QR scan response ke liye
from datetime import datetime

from teacher.models import StudentClassMembership
from .forms import StudentProfileUpdateForm
# Karan's Addition: Importing models for attendance calculation
from accounts.models import Attendance, Subject 
>>>>>>> 237c3ec7b9c4ac0db7f364399a5e1ec6901a1d98

@login_required
def student_dashboard(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access the student dashboard.")
        return redirect("login")

    memberships = _student_classrooms(request.user)

    enrolled_courses = [membership.classroom for membership in memberships]
    today_schedule = enrolled_courses[:5]
    unread_messages_count = Message.objects.filter(recipient=request.user, is_read=False).count()
    open_queries_count = Query.objects.filter(student=request.user, status=Query.STATUS_OPEN).count()

    # --- Karan's Work: Attendance Percentage Calculation ---
    # Hum saare subjects ke liye total classes aur attended classes nikaal rahe hain
    total_attended = Attendance.objects.filter(student=request.user).count()
    
    # Abhi ke liye hum total classes 100 maan rahe hain (Simulation purpose)
    # Ise tum baad mein dynamic bhi kar sakte ho
    total_classes = 100 
    attendance_percentage = (total_attended / total_classes) * 100 if total_classes > 0 else 0
    
    # Alert logic
    is_shortage = attendance_percentage < 75

    context = {
        "enrolled_courses": enrolled_courses,
        "today_schedule": today_schedule,
<<<<<<< HEAD
        "unread_messages_count": unread_messages_count,
        "open_queries_count": open_queries_count,
=======
        "total_attended": total_attended,
        "attendance_percentage": round(attendance_percentage, 2),
        "is_shortage": is_shortage, # Dashboard par red alert dikhane ke liye
>>>>>>> 237c3ec7b9c4ac0db7f364399a5e1ec6901a1d98
    }
    return render(request, "student/student_dashboard.html", context)


@login_required
def student_qr_attendance(request):
    """
    Karan's Work: This view will handle the actual QR data 
    sent from the scanner page.
    """
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")
    
    if request.method == "POST":
        qr_data = request.POST.get('qr_data') # Scanning page se data aayega
        
        try:
            # Example Data format: "TID:1|SID:2|TS:1711882800"
            parts = qr_data.split('|')
            subject_id = parts[1].split(':')[1]
            
            subject = Subject.objects.get(id=subject_id)
            
            # Database mein check/save karna
            # get_or_create ensures ki ek din mein ek hi baar attendance mark ho
            obj, created = Attendance.objects.get_or_create(
                student=request.user,
                subject=subject,
                date=datetime.now().date()
            )
            
            if created:
                return JsonResponse({'status': 'success', 'message': 'Attendance marked successfully!'})
            else:
                return JsonResponse({'status': 'info', 'message': 'Attendance already marked for today.'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid QR Code or Scan Error.'})

    # GET request par scanner page render hoga
    return render(request, "student/student_qr_attendance.html")


# --- Niche ke saare functions Backend 1 ke waise hi hain ---

@login_required
def student_profile_update(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")

    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("student_dashboard")
    else:
        form = StudentProfileUpdateForm(instance=request.user)

    return render(request, "student/student_profile_update.html", {"form": form})

@login_required
def student_performance(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")

    records = (
        Performance.objects
        .filter(student=request.user, classroom_id__in=_student_classroom_ids(request.user))
        .select_related("classroom", "classroom__teacher")
    )

    total_percentage = sum(record.percentage for record in records)
    average_percentage = round(total_percentage / records.count(), 2) if records.exists() else 0

    context = {
        "records": records,
        "average_percentage": average_percentage,
    }
    return render(request, "student/student_performance.html", context)

@login_required
def student_queries(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")

    if request.method == "POST":
        form = StudentQueryForm(request.POST, student=request.user)
        if form.is_valid():
            query = form.save(commit=False)
            query.student = request.user
            query.save()
            messages.success(request, "Your question has been submitted.")
            return redirect("student_queries")
    else:
        form = StudentQueryForm(student=request.user)

    queries = (
        Query.objects
        .filter(student=request.user, classroom_id__in=_student_classroom_ids(request.user))
        .select_related("classroom", "answered_by")
    )

    context = {
        "form": form,
        "queries": queries,
    }
    return render(request, "student/student_queries.html", context)

@login_required
def student_messages(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")

    if request.method == "POST":
        form = StudentMessageForm(request.POST, student=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, "Your message has been sent.")
            return redirect("student_messages")
    else:
        form = StudentMessageForm(student=request.user)

    classroom_ids = _student_classroom_ids(request.user)
    messages_qs = (
        Message.objects
        .filter(Q(sender=request.user) | Q(recipient=request.user) | Q(classroom_id__in=classroom_ids, recipient__isnull=True))
        .select_related("sender", "recipient", "classroom")
        .distinct()
    )

    context = {
        "form": form,
        "student_messages": messages_qs,
    }
    return render(request, "student/student_messages.html", context)

@login_required
def student_attendance(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")

    records = (
        Attendance.objects
        .filter(student=request.user, classroom_id__in=_student_classroom_ids(request.user))
        .select_related("classroom", "marked_by")
    )
    summary = records.values("status").annotate(total=Count("id"))
    total_classes = records.count()
    attended_classes = records.filter(status__in=[Attendance.STATUS_PRESENT, Attendance.STATUS_LATE]).count()
    attendance_percentage = round((attended_classes / total_classes) * 100, 2) if total_classes else 0

    context = {
        "records": records,
        "summary": summary,
        "total_classes": total_classes,
        "attended_classes": attended_classes,
        "attendance_percentage": attendance_percentage,
    }
    return render(request, "student/student_attendance.html", context)

@login_required
def student_announcements(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")
<<<<<<< HEAD

    now = timezone.now()
    announcements = (
        Announcement.objects
        .filter(classroom_id__in=_student_classroom_ids(request.user))
        .filter(Q(publish_at__isnull=True) | Q(publish_at__lte=now))
        .filter(Q(expires_at__isnull=True) | Q(expires_at__gte=now))
        .select_related("classroom", "posted_by")
    )

    return render(request, "student/student_announcements.html", {"announcements": announcements})


@login_required
def student_courses(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")

    classroom_ids = _student_classroom_ids(request.user)
    courses = (
        Course.objects
        .filter(classroom_id__in=classroom_ids, is_active=True)
        .select_related("subject", "classroom", "teacher")
    )

    fallback_classes = (
        StudentClassMembership.objects
        .filter(student=request.user, classroom_id__in=classroom_ids)
        .exclude(classroom__course__isnull=False)
        .select_related("classroom", "classroom__teacher")
    )

    context = {
        "courses": courses,
        "fallback_classes": fallback_classes,
    }
    return render(request, "student/student_courses.html", context)


@login_required
def student_qr_attendance(request):
    if request.user.role != "student":
        messages.error(request, "You are not allowed to access this page.")
        return redirect("login")
    return render(request, "student/student_qr_attendance.html")
=======
    return render(request, "student/student_announcements.html")
>>>>>>> 237c3ec7b9c4ac0db7f364399a5e1ec6901a1d98
