# tickets/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_number',
        'event',
        'attendee_name',
        'price',
        'quantity',
        'created_at',
        'qr_code_preview'
    ]
    
    list_filter = ['event', 'created_at']
    search_fields = [
        'ticket_number',
        'attendee_name',
        'attendee_email',
        'buyer__email'
    ]
    
    readonly_fields = [
        'ticket_number',
        'created_at',
        'qr_code_preview'
    ]
    
    raw_id_fields = ['event', 'ticket_type', 'buyer']
    
    fieldsets = (
        ('Informations du ticket', {
            'fields': ('ticket_number', 'event', 'ticket_type')
        }),
        ('Acheteur', {
            'fields': ('buyer',)
        }),
        ('Participant', {
            'fields': ('attendee_name', 'attendee_email')
        }),
        ('Caractéristiques', {
            'fields': ('price', 'quantity')
        }),
        ('Codes', {
            'fields': ('qr_code_preview',),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="50" height="50" />',
                obj.qr_code.url
            )
        return "Pas de QR code"
    qr_code_preview.short_description = "QR Code"
    
    actions = ['send_tickets_by_email']
    
    def send_tickets_by_email(self, request, queryset):
        from django.core.mail import send_mail
        from django.conf import settings
        
        count = 0
        for ticket in queryset:
            if ticket.attendee_email:
                send_mail(
                    subject=f'Votre ticket pour {ticket.event.title}',
                    message=f'Bonjour {ticket.attendee_name},\n\n'
                           f'Votre ticket {ticket.ticket_number} est disponible.\n'
                           f'Événement: {ticket.event.title}\n'
                           f'Date: {ticket.event.start_date}\n\n'
                           f'QR code disponible dans votre espace client.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[ticket.attendee_email],
                    fail_silently=True,
                )
                count += 1
        
        self.message_user(request, f'{count} tickets envoyés par email')
    send_tickets_by_email.short_description = "Envoyer les tickets par email"