from django.contrib import admin
from .models import User, UserProfile


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = [
        (
            "User Credentials",
            {"fields": ["email", "first_name", "last_name"]},
        ),
        (
            "Permissions",
            {"fields": ["is_active", "is_staff", "is_superuser"]},
        ),
    ]
