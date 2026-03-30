from django.conf import settings
from django.db import models


class TeacherClass(models.Model):
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=50, blank=True, null=True)
    subject_name = models.CharField(max_length=100, blank=True, null=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_classes",
        limit_choices_to={"role": "teacher"},
    )

    def __str__(self):
        if self.section:
            return f"{self.name} - {self.section}"
        return self.name


class StudentClassMembership(models.Model):
    classroom = models.ForeignKey(
        TeacherClass,
        on_delete=models.CASCADE,
        related_name="student_memberships",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="class_memberships",
        limit_choices_to={"role": "student"},
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("classroom", "student")

    def __str__(self):
        return f"{self.student.full_name} -> {self.classroom}"
