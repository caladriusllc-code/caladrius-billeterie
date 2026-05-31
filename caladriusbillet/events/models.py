from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  
import uuid

class EventCategory(models.TextChoices):
    CONCERT = 'concert', 'Concert'
    SPORT = 'sport', 'Sport'
    THEATER = 'theater', 'Théâtre'
    FESTIVAL = 'festival', 'Festival'
    CONFERENCE = 'conference', 'Conférence'
    WORKSHOP = 'workshop', 'Atelier'
    COMEDY = 'comedy', 'Comédie'
    KIDS = 'kids', 'Enfants'
    OTHER = 'other', 'Autre'

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    description = models.TextField(help_text='Description complète')
    category = models.CharField(max_length=50, choices=EventCategory.choices, default=EventCategory.OTHER)
    
    # Lieu
    venue_name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='France')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    capacity = models.PositiveIntegerField(help_text="Capacité maximale du lieu")    

    # Dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    sales_start_date = models.DateTimeField()
    sales_end_date = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']
        verbose_name = "Évènement"
        verbose_name_plural = "Évènements"
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'start_date'],
                name='unique_event_title_startdate'
            )
        ]

    def __str__(self):
        return f"{self.title} - {self.city}"

    def clean(self):
        """ Logique de validation personnalisée pour les dates """
        super().clean()
        errors = {}

        # 1. Fin de l'évènement VS Début de l'évènement
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                errors['end_date'] = "La date de fin doit être postérieure à la date de début."

        # 2. Fin des ventes VS Début des ventes
        if self.sales_start_date and self.sales_end_date:
            if self.sales_end_date <= self.sales_start_date:
                errors['sales_end_date'] = "La date de fin des ventes doit être postérieure à la date de début des ventes."

        # 3. Cohérence générale (ex: début des ventes avant l'événement)
        if self.sales_start_date and self.start_date:
            if self.sales_start_date >= self.start_date:
                errors['sales_start_date'] = "Le début des ventes doit avoir lieu avant le début de l'évènement."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """ Force l'exécution de la méthode clean() pour sécuriser l'API REST """
        self.full_clean()
        super().save(*args, **kwargs)


class TicketType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=100) # Ex: VIP, Régulier
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_initial = models.PositiveIntegerField(default=0) # Total mis en vente au départ
    quantity_available = models.PositiveIntegerField() # Ce qu'il reste actuellement
    max_per_order = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Type de ticket"
        verbose_name_plural = "Types de tickets"

    def __str__(self):
        return f"{self.name} - {self.price}€ ({self.event.title})"

    @property
    def tickets_sold(self):
        """ Calcule automatiquement le nombre de tickets vendus """
        # Sécurité pour éviter un calcul négatif involontaire
        if self.quantity_initial < self.quantity_available:  
            return 0
        return self.quantity_initial - self.quantity_available

    def clean(self):
        """ Sécurité : Empêche d'avoir plus de tickets disponibles que le stock de départ """
        super().clean()
        if self.quantity_available is not None and self.quantity_initial is not None:
            if self.quantity_available > self.quantity_initial:
                raise ValidationError({
                    'quantity_available': "La quantité disponible ne peut pas être supérieure à la quantité initiale."
                })

    def save(self, *args, **kwargs):
        """ Force l'exécution du clean pour ce modèle également """
        self.full_clean()
        super().save(*args, **kwargs)