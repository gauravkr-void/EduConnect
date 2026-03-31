from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("class/", views.teacher_class_view, name="teacher_class"),
    path("profile/update/", views.teacher_profile_update, name="teacher_profile_update"),
    path('generate-qr/<int:subject_id>/', views.generate_qr_view, name='generate_qr'),
]

