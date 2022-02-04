from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.


class UserProfile(AbstractUser):
    email = models.EmailField(_('email address'), blank=True, unique=True)
    image = models.ImageField(default='default.jpg', null=True,upload_to='accounts')
