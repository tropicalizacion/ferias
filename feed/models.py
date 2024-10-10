from django.db import models
from marketplaces.models import Marketplace
from datetime import datetime
from tinymce.models import HTMLField
from django.utils.text import slugify

# Create your models here.


class Event(models.Model):
    """
    Data model: https://schema.org/Event
    """

    event_slug = models.SlugField(max_length=200, blank=True, null=True)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.event_slug:
            self.event_slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class News(models.Model):
    """
    Data model: https://schema.org/NewsArticle
    """

    news_slug = models.SlugField(max_length=200, blank=True, null=True)
    marketplaces = models.ManyToManyField(Marketplace, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.news_slug:
            self.news_slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Alert(models.Model):
    """
    Data model: None
    """

    alert_slug = models.SlugField(max_length=200, blank=True, null=True)
    marketplaces = models.ManyToManyField(Marketplace, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    start_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to="alerts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.alert_slug:
            self.alert_slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
