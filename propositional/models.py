from django.db import models

from authenticator.models import VUser


# Create your models here.
class Proposition(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    place = models.TextField(null=True, blank=True)
    user = models.ForeignKey(VUser, on_delete=models.CASCADE, related_name='propositions', null=True, blank=True)

