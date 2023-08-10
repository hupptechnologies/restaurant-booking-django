from django.contrib import admin, messages
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'capacity']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'table', 'date', 'start_time', 'end_time', 'is_cancelled', 'guest']
    list_editable = ['table', 'date', 'start_time', 'end_time', 'is_cancelled']
    list_per_page = 5
    search_fields = ['customer_name', 'table', 'date', 'start_time', 'end_time', 'is_cancelled', 'guest']
    list_filter = ['guest','table','date','start_time','end_time','is_cancelled']
    actions = ["bulk_toggle_cancelled"]

    @admin.action(description="Cancel/Uncancel selected reservations")
    def bulk_toggle_cancelled(self, request, queryset):
        for obj in queryset:
            obj.is_cancelled = not obj.is_cancelled
            obj.save()

        self.message_user(
            request,
            "Successfully cancel/uncancel selected reservations",
            messages.SUCCESS,
        )