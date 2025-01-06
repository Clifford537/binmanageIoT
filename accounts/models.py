from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    MUNICIPAL = 'municipal_authority'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MUNICIPAL, 'Municipal Authority'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MUNICIPAL)
    
    def __str__(self):
        return self.username
