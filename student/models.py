from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from teacher.models import TeacherClass


class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="courses")
    classroom = models.OneToOneField(
        TeacherClass,
        on_delete=models.CASCADE,
        related_name="course",
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="taught_courses",
        limit_choices_to={"role": "teacher"},
    )
    academic_year = models.CharField(max_length=20, blank=True)
    semester = models.CharField(max_length=20, blank=True)
    room = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["subject__code", "classroom__name"]

    def __str__(self):
        return f"{self.subject.code} - {self.classroom}"


class Attendance(models.Model):
    STATUS_PRESENT = "present"
    STATUS_ABSENT = "absent"
    STATUS_LATE = "late"
    STATUS_EXCUSED = "excused"

    STATUS_CHOICES = (
        (STATUS_PRESENT, "Present"),
        (STATUS_ABSENT, "Absent"),
        (STATUS_LATE, "Late"),
        (STATUS_EXCUSED, "Excused"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        limit_choices_to={"role": "student"},
    )
    classroom = models.ForeignKey(TeacherClass, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PRESENT)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="marked_attendance_records",
        limit_choices_to={"role": "teacher"},
        blank=True,
        null=True,
    )
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "classroom__name"]
        unique_together = ("student", "classroom", "date")
        indexes = [
            models.Index(fields=["student", "classroom", "date"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.classroom} - {self.date}"


class Announcement(models.Model):
    PRIORITY_NORMAL = "normal"
    PRIORITY_IMPORTANT = "important"
    PRIORITY_URGENT = "urgent"

    PRIORITY_CHOICES = (
        (PRIORITY_NORMAL, "Normal"),
        (PRIORITY_IMPORTANT, "Important"),
        (PRIORITY_URGENT, "Urgent"),
    )

    classroom = models.ForeignKey(TeacherClass, on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField(max_length=160)
    body = models.TextField()
    priority = models.CharField(max_length=12, choices=PRIORITY_CHOICES, default=PRIORITY_NORMAL)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="posted_announcements",
        limit_choices_to={"role": "teacher"},
        blank=True,
        null=True,
    )
    publish_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(expires_at__isnull=True)
                    | models.Q(publish_at__isnull=True)
                    | models.Q(expires_at__gte=models.F("publish_at"))
                ),
                name="announcement_valid_publish_window",
            )
        ]

    def __str__(self):
        return self.title


class Message(models.Model):
    classroom = models.ForeignKey(
        TeacherClass,
        on_delete=models.CASCADE,
        related_name="messages",
        blank=True,
        null=True,
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
        blank=True,
        null=True,
    )
    subject = models.CharField(max_length=140)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"]),
            models.Index(fields=["classroom", "created_at"]),
        ]

    def __str__(self):
        return self.subject


class Query(models.Model):
    STATUS_OPEN = "open"
    STATUS_ANSWERED = "answered"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = (
        (STATUS_OPEN, "Open"),
        (STATUS_ANSWERED, "Answered"),
        (STATUS_CLOSED, "Closed"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="queries",
        limit_choices_to={"role": "student"},
    )
    classroom = models.ForeignKey(TeacherClass, on_delete=models.CASCADE, related_name="queries")
    title = models.CharField(max_length=160)
    question = models.TextField()
    answer = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_OPEN)
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="answered_queries",
        limit_choices_to={"role": "teacher"},
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["student", "status"]),
            models.Index(fields=["classroom", "status"]),
        ]

    def __str__(self):
        return self.title


class Performance(models.Model):
    ASSESSMENT_ASSIGNMENT = "assignment"
    ASSESSMENT_QUIZ = "quiz"
    ASSESSMENT_MIDTERM = "midterm"
    ASSESSMENT_FINAL = "final"
    ASSESSMENT_PROJECT = "project"

    ASSESSMENT_CHOICES = (
        (ASSESSMENT_ASSIGNMENT, "Assignment"),
        (ASSESSMENT_QUIZ, "Quiz"),
        (ASSESSMENT_MIDTERM, "Midterm"),
        (ASSESSMENT_FINAL, "Final"),
        (ASSESSMENT_PROJECT, "Project"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="performance_records",
        limit_choices_to={"role": "student"},
    )
    classroom = models.ForeignKey(TeacherClass, on_delete=models.CASCADE, related_name="performance_records")
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_CHOICES)
    title = models.CharField(max_length=160)
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    max_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1)])
    grade = models.CharField(max_length=5, blank=True)
    feedback = models.TextField(blank=True)
    recorded_at = models.DateField()
    weight = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Optional percentage weight for this assessment.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at", "classroom__name"]
        constraints = [
            models.CheckConstraint(check=models.Q(score__lte=models.F("max_score")), name="performance_score_lte_max_score"),
        ]
        indexes = [
            models.Index(fields=["student", "classroom", "recorded_at"]),
            models.Index(fields=["assessment_type"]),
        ]

    @property
    def percentage(self):
        if not self.max_score:
            return 0
        return round((self.score / self.max_score) * 100, 2)

    def __str__(self):
        return f"{self.student.full_name} - {self.title}"
