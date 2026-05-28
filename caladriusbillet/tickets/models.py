# tickets/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps
import uuid
import random
import string
from io import BytesIO
from django.core.files.base import ContentFile
import time

# Optionnel - Commentez si vous n'avez pas qrcode
# import qrcode

User = get_user_model()


class Guest(models.Model):
    """Modèle pour les invités/acheteurs sans compte"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    
    address = models.TextField(blank=True, null=True, verbose_name="Adresse")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ville")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Code postal")
    country = models.CharField(max_length=100, default='France', verbose_name="Pays")
    
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_purchase_at = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # ✅ SUPPRIMÉ : le champ guest qui était en trop
    
    class Meta:
        verbose_name = "Invité"
        verbose_name_plural = "Invités"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email'], name='guest_email_idx'),
            models.Index(fields=['phone'], name='guest_phone_idx'),
            models.Index(fields=['last_name', 'first_name'], name='guest_name_idx'),
        ]
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def total_purchases(self):
        Ticket = apps.get_model('tickets', 'Ticket')
        return Ticket.objects.filter(guest=self).count()
    
    def __str__(self):
        return f"{self.full_name} - {self.email}"


class Ticket(models.Model):
    """Modèle pour générer des tickets d'événements"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_number = models.CharField(max_length=50, unique=True, editable=False)
    qr_code = models.ImageField(upload_to='tickets/qrcodes/', blank=True, null=True)
    
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey('events.TicketType', on_delete=models.CASCADE, related_name='tickets')
    
    # ✅ CORRIGÉ : guest pointe vers Guest (pas User)
    guest = models.ForeignKey(
        Guest,  # ← Maintenant correct
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='tickets'
    )
    
    attendee_name = models.CharField(max_length=200)
    attendee_email = models.EmailField()
    attendee_phone = models.CharField(max_length=20, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    seat_number = models.CharField(max_length=20, blank=True, null=True)
    row_number = models.CharField(max_length=10, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
  
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        super().save(*args, **kwargs)
    
    def generate_ticket_number(self):
        prefix = self.event.slug[:4].upper() if self.event else "TKT"
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return f"{prefix}-{random_part}"
    
    def generate_qr_code(self):
        """Génère un QR code pour le ticket - Nécessite qrcode"""
        try:
            import qrcode
            qr_data = {
                'ticket_id': str(self.id),
                'ticket_number': self.ticket_number,
                'event': self.event.title,
                'event_date': str(self.event.start_date),
                'attendee': self.attendee_name,
            }
            
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(str(qr_data))
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            file_name = f"ticket_{self.ticket_number}.png"
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
            
        except ImportError:
            print("QR code non généré: bibliothèque qrcode non installée")
        except Exception as e:
            print(f"Erreur génération QR code: {e}")
    
    @property
    def purchaser_name(self):
        """Nom de l'acheteur"""
        if self.guest:
            return self.guest.full_name  # ✅ Maintenant fonctionne
        return self.attendee_name
    
    @property
    def purchaser_email(self):
        """Email de l'acheteur"""
        if self.guest:
            return self.guest.email  # ✅ Maintenant fonctionne
        return self.attendee_email
    
    def __str__(self):
        return f"{self.ticket_number} - {self.attendee_name}"


class Order(models.Model):
    """Commande de tickets"""
    
    STATUS_CHOICES = [
        ('pending', 'En attente de paiement'),
        ('paid', 'Payé'),
        ('cancelled', 'Annulé'),
        ('expired', 'Expiré'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    
    # ✅ Client - pointe vers Guest
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='orders')
    
    # Informations de la commande
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Paiement
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        random_part = ''.join(random.choices(string.digits, k=6))
        return f"CMD-{int(time.time())}-{random_part}"
    
    @property
    def total_tickets(self):
        return self.items.count()
    
    def __str__(self):
        return f"{self.order_number} - {self.guest.email} - {self.status}"


class OrderItem(models.Model):
    """Ligne de commande (un type de ticket)"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket_type = models.ForeignKey('events.TicketType', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.ticket_type.name} x {self.quantity}"