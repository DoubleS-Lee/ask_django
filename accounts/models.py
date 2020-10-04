from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=6, blank=True)  # , validators=[]
