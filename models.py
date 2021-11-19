from django.db import models
from django.contrib.auth.models import AbstractUser


class RocketCore(models.Model):
    core_id = models.TextField(max_length=6)
    reuse_count = models.IntegerField()
    total_payload_mass = models.IntegerField()


class User(AbstractUser):
    favorite_core = models.ForeignKey(RocketCore, on_delete=models.CASCADE, null=True, blank=True)
