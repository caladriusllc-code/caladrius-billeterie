from django.db import models
from django.contrib.auth import get_user_model
import uuid
import random
import string
import time
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings

User = get_user_model()


class Ticket(models.Model):
    """Modèle pour générer des tickets d'événements"""
    
    STATUS_CHOICES = [
        ('valid', 'Valide'),
        ('used', 'Utilisé'),
        ('cancelled', 'Annulé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_number = models.CharField(max_length=50, unique=True, editable=False)
    qr_code = models.ImageField(upload_to='tickets/qrcodes/', blank=True, null=True, editable=False)
    
    # ✅ AJOUT : Lien direct vers la commande et son statut
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='generated_tickets', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='valid')
    scanned_at = models.DateTimeField(null=True, blank=True)
    
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey('events.TicketType', on_delete=models.CASCADE, related_name='tickets')
    
    attendee_name = models.CharField(max_length=200)
    attendee_email = models.EmailField()
    attendee_phone = models.CharField(max_length=20, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat_number = models.CharField(max_length=20, blank=True, null=True)
    row_number = models.CharField(max_length=10, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
  
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # 1. Assurer la génération du numéro de ticket
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        
        # 2. 🔥 FIX : Générer le QR code AVANT de sauvegarder en BDD
        if not self.qr_code:
            self.generate_qr_code()
            
        super().save(*args, **kwargs)
    
    def generate_ticket_number(self):
        prefix = self.event.slug[:4].upper() if self.event and getattr(self.event, 'slug', None) else "TKT"
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return f"{prefix}-{random_part}"
    
    def generate_qr_code(self):
        """Génère un QR code sécurisé pour le ticket"""
        try:
            import qrcode
            
            # 🔥 SÉCURITÉ : On ne met QUE l'ID (UUID) unique dans le QR Code.
            # L'application de scan interrogera le backend avec cet ID pour éviter la fraude.
            qr_data = str(self.id)
            
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            file_name = f"ticket_{self.ticket_number}.png"
            
            # save=False pour éviter une récursion/boucle infinie sur la méthode save()
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
            
        except ImportError:
            print("QR code non généré: bibliothèque qrcode non installée")
        except Exception as e:
            print(f"Erreur génération QR code: {e}")
    
    @property
    def purchaser_name(self):
        """Nom de l'acheteur (via la commande s'il y en a une, sinon le participant)"""
        if self.order and self.order.guest:
            return self.order.guest.full_name
        return self.attendee_name
    
    @property
    def purchaser_email(self):
        """Email de l'acheteur"""
        if self.order and self.order.guest:
            return self.order.guest.email
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
    
    # ✅ CORRECTION : On pointe directement vers l'utilisateur Django
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    
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
        return f"{self.order_number} - {self.user.email} - {self.status}"


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