from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("profile/update/", views.student_profile_update, name="student_profile_update"),
    path("qr-attendance/", views.student_qr_attendance, name="student_qr_attendance"),
    path("performance/", views.student_performance, name="student_performance"),
    path("queries/", views.student_queries, name="student_queries"),
    path("messages/", views.student_messages, name="student_messages"),
    path("attendance/", views.student_attendance, name="student_attendance"),
    path("announcements/", views.student_announcements, name="student_announcements"),
]
