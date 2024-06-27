from django.db import models
from marketplaces.models import Marketplace
from django.contrib.auth.models import User

# Create your models here.


class MarketplaceAdmin(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"

class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"