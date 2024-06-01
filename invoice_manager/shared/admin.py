from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    exclude = ("creator",)
    readonly_fields = ("created_at", "updated_at")

class BaseTabularInline(admin.TabularInline):
    exclude = ("creator", "created_at", "updated_at")
