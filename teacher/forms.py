from django import forms
from accounts.models import User

from .models import StudentClassMembership, TeacherClass


class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "contact_number",
            "institution_name",
            "department",
            "employee_id",
            "profile_picture",
        ]


class TeacherClassForm(forms.ModelForm):
    class Meta:
        model = TeacherClass
        fields = ["name", "subject_name", "section", "academic_year"]
        labels = {
            "name": "Class Name",
            "subject_name": "Subject",
            "academic_year": "Academic Year",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Example: BCA Semester 4"}),
            "subject_name": forms.TextInput(attrs={"placeholder": "Example: Database Management"}),
            "section": forms.TextInput(attrs={"placeholder": "Example: Section D"}),
            "academic_year": forms.TextInput(attrs={"placeholder": "Example: 2026"}),
        }


class AddStudentToClassForm(forms.ModelForm):
    class Meta:
        model = StudentClassMembership
        fields = ["student"]

    def __init__(self, *args, classroom=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.classroom = classroom
        students = User.objects.filter(role="student").order_by("full_name", "email")
        if classroom is not None:
            enrolled_student_ids = StudentClassMembership.objects.filter(classroom=classroom).values_list("student_id", flat=True)
            students = students.exclude(id__in=enrolled_student_ids)
        self.fields["student"].queryset = students
        self.fields["student"].label = "Student"
        self.fields["student"].empty_label = "Select a student"

    def save(self, commit=True):
        membership = super().save(commit=False)
        membership.classroom = self.classroom
        if commit:
            membership.save()
        return membership
