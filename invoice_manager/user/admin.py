from django.contrib import admin
from django.utils.translation import gettext as _

from user.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number")
    search_fields = ("phone_number")

    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "phone_number",
                    "address",
                )
            },
        ),
    )
    search_fields = ("email", "phone_number")
    readonly_fields = ("last_login", "date_joined")
