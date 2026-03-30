from django import forms
from accounts.models import User


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
