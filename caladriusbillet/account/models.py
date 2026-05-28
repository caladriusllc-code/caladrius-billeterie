from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True) 
    city = models.CharField(max_length=100, blank=True, null=True) 
    country = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    ROLE_CHOICES = (  # Majuscule + corrigé
        ('organisateur', 'Organisateur'),
        ('utilisateur', 'Utilisateur'),
        ('admin', 'Administrateur'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='utilisateur')
    is_organisateur = models.BooleanField(default=False)
    organisation_name = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Synchronisation automatique
        self.is_organisateur = (self.role == 'organisateur')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"  # get_role_display() donne la valeur affichée
    

