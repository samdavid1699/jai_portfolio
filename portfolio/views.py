
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Project, ContactMessage


def home(request):
    projects = Project.objects.all().order_by("-featured", "-id")

    skills = [
        "Python",
        "Django",
        "HTML5",
        "CSS3",
        "JavaScript",
        "Bootstrap",
        "SQLite",
        "MySQL",
        "CRUD Operations",
        "REST APIs",
        "Git",
        "GitHub",
    ]

    context = {
        "projects": projects,
        "skills": skills,
    }

    return render(request, "portfolio/home.html", context)


@require_POST
def contact(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()

    if not all([name, email, subject, message]):
        messages.error(request, "Please fill in all fields.")
        return redirect("home")

    if (
        len(name) > 100
        or len(email) > 254
        or len(subject) > 150
        or len(message) > 10000
    ):
        messages.error(request, "One or more fields are too long.")
        return redirect("home")

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Please enter a valid email address.")
        return redirect("home")

    ContactMessage.objects.create(
        name=name,
        email=email,
        subject=subject,
        message=message,
    )

    messages.success(
        request,
        "Thank you for contacting me! Your message has been received."
    )

    return redirect("home")
