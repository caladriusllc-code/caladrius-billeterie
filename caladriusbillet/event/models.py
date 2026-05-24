from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  # Import nécessaire pour les erreurs
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
    
    # Timestamps
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
        """
        Logique de validation personnalisée pour les dates.
        """
        # On appelle d'abord la méthode clean parente
        super().clean()

        errors = {}

        # 1. Vérification : Fin de l'évènement VS Début de l'évènement
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                errors['end_date'] = "La date de fin doit être postérieure à la date de début."

        # 2. Vérification : Fin des ventes VS Début des ventes
        if self.sales_start_date and self.sales_end_date:
            if self.sales_end_date <= self.sales_start_date:
                errors['sales_end_date'] = "La date de fin des ventes doit être postérieure à la date de début des ventes."

        # 3. Vérification : Cohérence générale (ex: on commence à vendre avant que l'évènement ne commence)
        if self.sales_start_date and self.start_date:
            if self.sales_start_date >= self.start_date:
                errors['sales_start_date'] = "Le début des ventes doit avoir lieu avant le début de l'évènement."

        # Si le dictionnaire d'erreurs n'est pas vide, on lève l'exception
        if errors:
            raise ValidationError(errors)