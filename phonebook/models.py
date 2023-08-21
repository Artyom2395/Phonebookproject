from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    work_phone = models.CharField(max_length=20)
    personal_phone = models.CharField(max_length=20)