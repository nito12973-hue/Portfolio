from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("a-propos/", views.about, name="about"),
    path("competences/", views.skills, name="skills"),
    path("projets/", views.projects, name="projects"),
    path("projets/<int:project_id>/", views.project_detail, name="project_detail"),
    path("formation/", views.formation, name="formation"),
    path("contact/", views.contact, name="contact"),
]
