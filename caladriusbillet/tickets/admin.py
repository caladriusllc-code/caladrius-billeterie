# tickets/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'event', 'attendee_name', 'price', 'qr_code_preview', 'created_at']
    list_filter = ['event', 'created_at']
    search_fields = ['ticket_number', 'attendee_name', 'attendee_email']
    readonly_fields = ['ticket_number', 'qr_code_preview', 'created_at']
    
    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50" />', obj.qr_code.url)
        return "Pas de QR code"
    qr_code_preview.short_description = "QR Code"
    