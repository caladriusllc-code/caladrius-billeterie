# tickets/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
import random
import string

User = get_user_model()


class Ticket(models.Model):
    """Modèle simple pour les tickets"""
    
    # Identifiants
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_number = models.CharField(max_length=50, unique=True, editable=False)
    
    # Relations
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey('events.TicketType', on_delete=models.CASCADE, related_name='tickets')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    
    # Informations
    attendee_name = models.CharField(max_length=200)
    attendee_email = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        super().save(*args, **kwargs)
    
    def generate_ticket_number(self):
        """Génère un numéro de ticket unique"""
        prefix = self.event.slug[:4].upper() if self.event else "TKT"
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"{prefix}-{random_part}"
    
    def __str__(self):
        return f"{self.ticket_number} - {self.attendee_name}"