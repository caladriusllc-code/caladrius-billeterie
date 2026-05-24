from django.db import models

# Create your models here.
class TicketType(models.Model):
    """Type de ticket (VIP, Normal, Étudiant, etc.)"""
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=100)  # VIP, Normal, Early Bird
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)
    max_per_order = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    includes_vat = models.BooleanField(default=True)
    requires_id_verification = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.price}€"
    
    @property
    def quantity_remaining(self):
        return self.quantity_available - self.quantity_sold
    
    @property
    def is_available(self):
        return self.is_active and self.quantity_remaining > 0