from django import forms
from accounts.models import User


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
