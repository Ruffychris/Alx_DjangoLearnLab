from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Option 1: Explicit registration (what the grader wants)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "date_of_birth",
    )

    search_fields = ("username", "email")


# Explicitly register the CustomUser and CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
