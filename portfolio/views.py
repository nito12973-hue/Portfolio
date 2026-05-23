from itertools import groupby
from operator import attrgetter

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactMessageForm
from .models import Education, Interest, Profile, Project, Skill


def _group_skills():
    skills = Skill.objects.order_by("category", "order", "name")
    grouped = []
    for category, items in groupby(skills, key=attrgetter("category")):
        grouped.append({"category": category, "items": list(items)})
    return grouped


def home(request):
    profile = Profile.get_solo()
    context = {
        "profile": profile,
        "featured_projects": Project.objects.filter(featured=True).order_by("-updated_at")[:3],
        "latest_projects": Project.objects.order_by("-created_at")[:3],
        "culture": Interest.objects.order_by("order")[:4],
        "grouped_skills": _group_skills()[:3],
        "project_count": Project.objects.count(),
        "skill_count": Skill.objects.count(),
    }
    return render(request, "home/index.html", context)


def about(request):
    profile = Profile.get_solo()
    return render(
        request,
        "home/about.html",
        {
            "profile": profile,
            "education": Education.objects.order_by("order"),
            "interests": Interest.objects.order_by("order"),
        },
    )


def skills(request):
    return render(
        request,
        "home/skills.html",
        {
            "profile": Profile.get_solo(),
            "grouped_skills": _group_skills(),
        },
    )


def projects(request):
    return render(
        request,
        "home/projects.html",
        {
            "profile": Profile.get_solo(),
            "projects": Project.objects.all(),
        },
    )


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(
        request,
        "home/project_detail.html",
        {
            "profile": Profile.get_solo(),
            "project": project,
            "projects": Project.objects.all(),
        },
    )


def formation(request):
    profile = Profile.get_solo()
    return render(
        request,
        "home/formation.html",
        {
            "profile": profile,
            "education": Education.objects.order_by("order"),
        },
    )


def contact(request):
    profile = Profile.get_solo()
    form = ContactMessageForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Merci ! Votre message a bien été reçu. Je reviens vers vous rapidement.")
        return redirect("portfolio:contact")

    return render(
        request,
        "home/contact.html",
        {
            "profile": profile,
            "form": form,
        },
    )
