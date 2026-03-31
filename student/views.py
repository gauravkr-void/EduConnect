from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import JsonResponse # QR scan response ke liye
from datetime import datetime

from teacher.models import StudentClassMembership
from .forms import StudentProfileUpdateForm
# Karan's Addition: Importing models for attendance calculation
from accounts.models import Attendance, Subject 

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
        "total_attended": total_attended,
        "attendance_percentage": round(attendance_percentage, 2),
        "is_shortage": is_shortage, # Dashboard par red alert dikhane ke liye
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