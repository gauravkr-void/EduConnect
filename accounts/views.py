from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, StudentRegistrationForm, TeacherRegistrationForm


def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == "teacher":
            return redirect("teacher_dashboard")
        return redirect("student_dashboard")

    selected_role = request.GET.get("role", "student")

    if request.method == "POST":
        form = LoginForm(request.POST)
        selected_role = request.POST.get("role", "student")

        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)

            if not form.cleaned_data.get("remember_me"):
                request.session.set_expiry(0)

            if user.role == "teacher":
                return redirect("teacher_dashboard")
            return redirect("student_dashboard")
    else:
        form = LoginForm(initial={"role": selected_role})

    context = {
        "form": form,
        "selected_role": selected_role,
    }
    return render(request, "accounts/login.html", context)


def register_view(request):
    selected_role = request.GET.get("role", "student")

    if selected_role == "teacher":
        form_class = TeacherRegistrationForm
    else:
        selected_role = "student"
        form_class = StudentRegistrationForm

    if request.method == "POST":
        selected_role = request.POST.get("role", "student")

        if selected_role == "teacher":
            form_class = TeacherRegistrationForm
        else:
            selected_role = "student"
            form_class = StudentRegistrationForm

        form = form_class(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, f"{selected_role.title()} account created successfully. Please log in.")
            return redirect(f"/login/?role={selected_role}")
    else:
        form = form_class()

    context = {
        "form": form,
        "selected_role": selected_role,
    }
    return render(request, "accounts/register.html", context)


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")
