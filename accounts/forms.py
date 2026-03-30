from django import forms
from django.contrib.auth import authenticate
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.CharField(widget=forms.HiddenInput())
    remember_me = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        role = cleaned_data.get("role")

        if email and password and role:
            user = authenticate(username=email, password=password)

            if not user:
                raise forms.ValidationError("Invalid email or password.")

            if user.role != role:
                raise forms.ValidationError("You selected the wrong login type for this account.")

            cleaned_data["user"] = user

        return cleaned_data


class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "password",
            "confirm_password",
            "roll_number",
            "course_year",
            "section_batch",
            "contact_number",
            "profile_picture",
            "terms_accepted",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        terms_accepted = cleaned_data.get("terms_accepted")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if not terms_accepted:
            raise forms.ValidationError("You must accept the terms and conditions.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class TeacherRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "password",
            "confirm_password",
            "institution_name",
            "department",
            "employee_id",
            "contact_number",
            "profile_picture",
            "terms_accepted",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        terms_accepted = cleaned_data.get("terms_accepted")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if not terms_accepted:
            raise forms.ValidationError("You must accept the terms and conditions.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "teacher"
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
