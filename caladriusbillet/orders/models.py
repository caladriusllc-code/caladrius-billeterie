import uuid
import time
import random
import string
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.conf import settings
from django.utils import timezone
from events.models import Event

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
    
    # Le user devient optionnel pour permettre l'achat anonyme (sans compte)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    
    # Informations obligatoires pour l'acheteur anonyme
    guest_email = models.EmailField(max_length=255, blank=True, null=True, help_text="Email de l'acheteur invité")
    guest_name = models.CharField(max_length=150, blank=True, null=True, help_text="Nom/Prénom de l'acheteur invité")
    
    # Informations complémentaires de la commande
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Suivi Paiement
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Dates de cycle de vie
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        random_part = ''.join(random.choices(string.digits, k=6))
        return f"CMD-{int(time.time())}-{random_part}"
    
    @property
    def total_tickets(self):
        # Somme des quantités de toutes les lignes
        return sum(item.quantity for item in self.items.all())
    
    def __str__(self):
        # ✅ CORRECTION SÉCURITÉ : Évite le crash si self.user est None (Achat invité)
        buyer_email = self.user.email if self.user else self.guest_email
        return f"{self.order_number} - {buyer_email} - {self.status}"


class OrderItem(models.Model):
    """Ligne de commande (un type de ticket et sa quantité)"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket_type = models.ForeignKey('events.TicketType', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    
    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commandes"

    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.ticket_type.name} x {self.quantity} (CMD: {self.order.order_number})"


class Ticket(models.Model):
    """Le Billet unique physique/numérique doté du QR Code à scanner à l'entrée"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='tickets')
    holder_name = models.CharField(max_length=200, blank=True, help_text="Nom de l'invité ou du porteur du billet")
    
    # Sécurité & Identification par QR Code
    unique_code = models.CharField(max_length=100, unique=True, editable=False)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    # Suivi du scan à l'entrée du concert
    is_scanned = models.BooleanField(default=False)
    scanned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Ticket individuel"
        verbose_name_plural = "Tickets individuels"

    def __str__(self):
        return f"Billet {self.unique_code} - {self.order_item.ticket_type.name}"

    def save(self, *args, **kwargs):
        """ Génère automatiquement un code de sécurité unique et son QR code lors de la création """
        if not self.unique_code:
            # Création d'un code unique unique et lisible (Ex: TCK-A1B2C3D4E5F6)
            self.unique_code = f"TCK-{uuid.uuid4().hex.upper()[:12]}"
            
            # Initialisation du générateur de QR Code
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(self.unique_code) # On encode le code unique à l'intérieur
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Sauvegarde du flux de l'image dans le champ ImageField de Django
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            filename = f"qr-{self.unique_code}.png"
            self.qr_code_image.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)