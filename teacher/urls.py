from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("class/", views.teacher_class_view, name="teacher_class"),
    path("class/<int:class_id>/", views.teacher_class_detail, name="teacher_class_detail"),
    path("class/<int:class_id>/edit/", views.teacher_class_edit, name="teacher_class_edit"),
    path(
        "class/<int:class_id>/remove-student/<int:membership_id>/",
        views.teacher_class_remove_student,
        name="teacher_class_remove_student",
    ),
    path("profile/update/", views.teacher_profile_update, name="teacher_profile_update"),
    path('generate-qr/<int:subject_id>/', views.generate_qr_view, name='generate_qr'),
]

