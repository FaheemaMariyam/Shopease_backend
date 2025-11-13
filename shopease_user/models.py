from django.db import models

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=20, default='user')  # admin/user
    blocked = models.BooleanField(default=False)
    # Override the save method to automatically set username = email(method override) 
    # if username is not provided (helps keep login consistent using email)
    def save(self, *args, **kwargs):
        if self.email and not self.username:
            self.username = self.email
         # automatically set role
        if self.is_staff or self.is_superuser:
            self.role = "admin"
        else:
            self.role = "user"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.username})"

