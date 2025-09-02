from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase


class HomePage(Page):
    """Simple homepage for Wagtail-driven content."""

    intro = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["wagtailcore.Page"]  # allow under root
    subpage_types = ["cms_pages.InfoPage", "cms_pages.BlogIndexPage"]


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


class BlogIndexPage(Page):
    """Container page that lists blog posts."""

    intro = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["cms_pages.HomePage"]
    subpage_types = ["cms_pages.BlogPostPage"]

    # For search
    search_fields = Page.search_fields + [
        index.SearchField("intro"),
    ]


class BlogPostPageTag(TaggedItemBase):
    """Tags for BlogPostPage using taggit + modelcluster."""

    content_object = ParentalKey(
        "cms_pages.BlogPostPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogPostPage(Page):
    """A single blog post."""

    date = models.DateField("Fecha de publicación")
    # Reuse existing author model; optional
    author = models.ForeignKey(
        "users.Author",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_posts",
    )
    intro = models.TextField(blank=True)
    body = RichTextField(blank=True)
    read_time = models.PositiveIntegerField("Tiempo de lectura (min)", default=3)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_post_images",
    )
    tags = ClusterTaggableManager(through=BlogPostPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("author"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("read_time"),
        FieldPanel("main_image"),
        FieldPanel("tags"),
    ]

    parent_page_types = ["cms_pages.BlogIndexPage"]
    subpage_types: list[str] = []

    # For search
    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

