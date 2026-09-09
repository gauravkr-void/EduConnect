from django import forms
from accounts.models import User
from teacher.models import StudentClassMembership

from .models import Message, Query


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "contact_number",
            "roll_number",
            "course_year",
            "section_batch",
            "profile_picture",
        ]


class StudentQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ["classroom", "title", "question"]
        widgets = {
            "question": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, student=None, **kwargs):
        super().__init__(*args, **kwargs)
        if student is not None:
            classroom_ids = StudentClassMembership.objects.filter(student=student).values_list("classroom_id", flat=True)
            self.fields["classroom"].queryset = self.fields["classroom"].queryset.filter(id__in=classroom_ids)


class StudentMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["classroom", "recipient", "subject", "body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, student=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.student = student
        if student is not None:
            memberships = StudentClassMembership.objects.filter(student=student).select_related("classroom", "classroom__teacher")
            classrooms = [membership.classroom for membership in memberships]
            teacher_ids = {classroom.teacher_id for classroom in classrooms}
            self.fields["classroom"].queryset = self.fields["classroom"].queryset.filter(id__in=[classroom.id for classroom in classrooms])
            self.fields["recipient"].queryset = User.objects.filter(id__in=teacher_ids, role="teacher")
        self.fields["classroom"].required = True
        self.fields["recipient"].required = True

    def clean(self):
        cleaned_data = super().clean()
        classroom = cleaned_data.get("classroom")
        recipient = cleaned_data.get("recipient")

        if classroom and recipient and classroom.teacher_id != recipient.id:
            raise forms.ValidationError("Select the teacher assigned to this class.")

        return cleaned_data
