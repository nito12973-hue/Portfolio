from django.contrib import admin

from .models import ContactMessage, Education, Interest, Profile, Project, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "phone", "location")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return not Profile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_filter = ("category",)
    ordering = ("category", "order", "name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "link", "created_at")
    list_filter = ("featured",)
    search_fields = ("title", "technologies")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "order")
    ordering = ("order", "-id")


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order", "name")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("name", "email", "message", "created_at")
    ordering = ("-created_at",)
