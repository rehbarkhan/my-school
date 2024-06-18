from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
# Create your models here.

class User(AbstractUser):
    login_failed_attempt = models.PositiveSmallIntegerField(default=0)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return str(self.email)

class AuthenticationLog(models.Model):
    email = models.EmailField()
    logged_in = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=256)
    is_success = models.BooleanField(default=None)
    
    def __str__(self):
        return str(self.email)

    class Meta:
        ordering = ['-logged_in']

class AccountRecovery(models.Model):
    email = models.EmailField()
    token_validity_till = models.DateTimeField(blank=True)
    token = models.CharField(max_length=256, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)
    is_forget = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email)
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.is_locked:
                self.token_validity_till = timezone.now() + timedelta(days=1)
            else:
                self.token_validity_till = timezone.now() + timedelta(minutes=30)
            self.token = get_random_string(256)
            return super(AccountRecovery, self).save(*args, **kwargs)
        raise ValidationError("Update operation is not allowed.")
