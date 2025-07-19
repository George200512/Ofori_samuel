from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 

from.models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ["user_name",  "email",  "date_added"]
    list_filter = ["is_active",  "is_admin"]
    ordering = ["user_name"]
    fieldsets = (
        (None, {"fields":("user_name",  "email",  "password")}), 
        ("Permissions", {"fields":("is_active", "is_admin")})
    )
    add_fieldsets = (
        (None, {"classes":("wide",), "fields":("user_name",  "email",  "password")}), 
    )

admin.site.register(User, CustomUserAdmin)