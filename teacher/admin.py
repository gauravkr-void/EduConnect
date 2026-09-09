from django.contrib import admin
from .models import StudentClassMembership, TeacherClass


@admin.register(TeacherClass)
class TeacherClassAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "subject_name", "academic_year", "teacher")
    list_filter = ("academic_year", "section", "teacher")
    search_fields = ("name", "section", "subject_name", "academic_year", "teacher__full_name", "teacher__email")


@admin.register(StudentClassMembership)
class StudentClassMembershipAdmin(admin.ModelAdmin):
    list_display = ("student", "classroom", "joined_at")
    search_fields = ("student__full_name", "student__email", "student__roll_number", "classroom__name")
