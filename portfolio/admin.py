from django.contrib import admin
from django.utils.html import format_html

from .models import ContactMessage, Education, Interest, Profile, Project, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "phone", "location", "created_at")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Informations personnelles", {
            "fields": ("name", "title", "avatar")
        }),
        ("Contact", {
            "fields": ("email", "phone", "location", "github")
        }),
        ("Description", {
            "fields": ("description",)
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def has_add_permission(self, request):
        return not Profile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_filter = ("category",)
    search_fields = ("name", "category")
    ordering = ("category", "order", "name")
    list_per_page = 25


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "get_technologies_preview", "created_at")
    list_filter = ("featured", "created_at")
    search_fields = ("title", "description", "technologies")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    fieldsets = (
        ("Informations du projet", {
            "fields": ("title", "description", "image", "featured")
        }),
        ("Technologies et liens", {
            "fields": ("technologies", "link")
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def get_technologies_preview(self, obj):
        technologies = obj.technology_list[:3]
        return format_html(", ".join(technologies))
    get_technologies_preview.short_description = "Technologies"


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "order")
    search_fields = ("title", "institution", "description")
    ordering = ("order", "-id")
    list_per_page = 20


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)
    ordering = ("order", "name")
    list_per_page = 25


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("name", "email", "message", "created_at")
    ordering = ("-created_at",)
    list_per_page = 20
    fieldsets = (
        ("Message", {
            "fields": ("name", "email", "message")
        }),
        ("Métadonnées", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )
