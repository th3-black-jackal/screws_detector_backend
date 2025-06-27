from django.contrib import admin
from .models import Machine

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display  = ("name", "status", "is_active", "last_heartbeat")
    search_fields = ("name",)
    list_filter   = ("status", "is_active")
