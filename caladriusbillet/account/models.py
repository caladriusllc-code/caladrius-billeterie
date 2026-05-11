from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import uuid
# Create your models here.

class CustomUser(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    adress = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True) 
    country = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    