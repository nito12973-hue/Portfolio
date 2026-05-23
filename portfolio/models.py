from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(TimestampedModel):
    name = models.CharField(max_length=100, default="Lamarana Diallo")
    title = models.CharField(max_length=150, default="Développeur Web & Administrateur de Bases de Données")
    description = models.TextField(
        default=(
            "Je construis des interfaces web modernes tout en assurant la sécurité et la performance des bases de données."
        )
    )
    email = models.EmailField(default="lamaranamamadousdiallo@gmail.com")
    phone = models.CharField(max_length=30, default="+221 77 536 5983")
    github = models.URLField(default="https://github.com/nito12973-hue")
    avatar = models.ImageField(upload_to="profiles/", blank=True, null=True)
    location = models.CharField(max_length=120, blank=True, default="Dakar, Sénégal")

    class Meta:
        verbose_name = _("Profil")
        verbose_name_plural = _("Profils")

    def __str__(self):
        return self.name

    @property
    def normalized_phone(self):
        return "".join(ch for ch in self.phone if ch.isdigit() or ch == "+")

    @classmethod
    def get_solo(cls):
        defaults = {
            "description": (
                "Je construis des interfaces web modernes tout en assurant la sécurité et la performance des bases de données."
            ),
            "github": "https://github.com/nito12973-hue",
            "email": "lamaranamamadousdiallo@gmail.com",
            "phone": "+221 77 536 5983",
            "location": "Dakar, Sénégal",
        }
        profile, _ = cls.objects.get_or_create(pk=1, defaults=defaults)
        return profile


class Skill(models.Model):
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=80, default="Général")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(TimestampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    technologies = models.JSONField(default=list, blank=True)
    link = models.URLField()
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-featured", "-created_at"]
        verbose_name = _("Projet")
        verbose_name_plural = _("Projets")

    def __str__(self):
        return self.title

    @property
    def technology_list(self):
        return self.technologies or []


class Education(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    institution = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = _("Formation")
        verbose_name_plural = _("Formations")

    def __str__(self):
        return self.title


class Interest(models.Model):
    name = models.CharField(max_length=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = _("Centre d'intérêt")
        verbose_name_plural = _("Centres d'intérêt")

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Message de contact")
        verbose_name_plural = _("Messages de contact")

    def __str__(self):
        return f"{self.name} — {self.email}"
