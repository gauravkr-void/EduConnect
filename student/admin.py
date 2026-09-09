from django.contrib import admin

from .models import Announcement, Attendance, Course, Message, Performance, Query, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("subject", "classroom", "teacher", "academic_year", "semester", "is_active")
    list_filter = ("is_active", "academic_year", "semester", "teacher")
    search_fields = ("subject__code", "subject__name", "classroom__name", "teacher__full_name")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "classroom", "date", "status", "marked_by")
    list_filter = ("status", "date", "classroom")
    search_fields = ("student__full_name", "student__email", "classroom__name")
    date_hierarchy = "date"


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "classroom", "priority", "posted_by", "created_at")
    list_filter = ("priority", "classroom", "created_at")
    search_fields = ("title", "body", "classroom__name")
    date_hierarchy = "created_at"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "recipient", "classroom", "is_read", "created_at")
    list_filter = ("is_read", "classroom", "created_at")
    search_fields = ("subject", "body", "sender__full_name", "recipient__full_name")
    date_hierarchy = "created_at"


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "classroom", "status", "answered_by", "updated_at")
    list_filter = ("status", "classroom", "updated_at")
    search_fields = ("title", "question", "answer", "student__full_name")
    date_hierarchy = "updated_at"


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("student", "classroom", "assessment_type", "title", "score", "max_score", "grade", "recorded_at")
    list_filter = ("assessment_type", "classroom", "recorded_at")
    search_fields = ("student__full_name", "student__email", "title", "classroom__name")
    date_hierarchy = "recorded_at"
