
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


class HomePage(Page):
    """Página principal del sitio"""
    
    hero_title = models.CharField(
        "Título principal", 
        max_length=255, 
        default="Bienvenido a deferia.cr"
    )
    hero_subtitle = RichTextField(
        "Subtítulo", 
        blank=True,
        help_text="Descripción que aparece debajo del título principal"
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagen principal"
    )
    
    # Secciones de contenido usando StreamField
    content_sections = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('marketplace_showcase', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('description', blocks.TextBlock()),
            ('show_featured', blocks.BooleanBlock(required=False)),
        ])),
    ], blank=True, verbose_name="Secciones de contenido")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
        ], heading="Sección Principal"),
        FieldPanel('content_sections'),
    ]

    class Meta:
        verbose_name = "Página Principal"


class ContentPage(Page):
    """Página de contenido general"""
    
    intro = RichTextField(
        "Introducción",
        blank=True,
        help_text="Texto introductorio de la página"
    )
    
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('embed', blocks.RawHTMLBlock()),
    ], blank=True, verbose_name="Contenido")
    
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagen destacada"
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('featured_image'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Página de Contenido"


class BlogPage(Page):
    """Página de entrada de blog"""
    
    date = models.DateField("Fecha de publicación")
    intro = models.CharField(max_length=250, verbose_name="Introducción")
    body = RichTextField(verbose_name="Contenido")
    
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagen destacada"
    )
    
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Etiquetas separadas por comas"
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('tags'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('featured_image'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('tags'),
    ]

    class Meta:
        verbose_name = "Entrada de Blog"


class BlogIndexPage(Page):
    """Página índice del blog"""
    
    intro = RichTextField(blank=True, verbose_name="Introducción")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    class Meta:
        verbose_name = "Índice del Blog"