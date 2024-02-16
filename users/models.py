from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email_address"), unique=True)
    username = models.CharField(max_length=150,unique=True,null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    avatar = models.ImageField(upload_to="users/avatars/",blank=True,null=True)
    bio = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    objects = CustomUserManager()
    def __str__(self):
        return self.email
