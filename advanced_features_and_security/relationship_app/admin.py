from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("date_of_birth", "profile_photo")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": ("date_of_birth", "profile_photo")
        }),
    )

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomUser, CustomUserAdmin)
