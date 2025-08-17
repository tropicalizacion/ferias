from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    """Simple homepage for Wagtail-driven content."""

    intro = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["wagtailcore.Page"]  # allow under root
    subpage_types = ["cms_pages.InfoPage"]


class InfoPage(Page):
    """Generic content page."""

    intro = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["cms_pages.HomePage"]
    subpage_types: list[str] = []
