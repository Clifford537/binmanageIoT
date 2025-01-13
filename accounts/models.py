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


class EmailNotification(models.Model):
    sender = models.EmailField()
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Field to mark as read

    def __str__(self):
        return f"Notification to {self.recipient} about {self.subject}"
