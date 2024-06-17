from django.db import models
from django.contrib.auth.models import AbstractUser
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
