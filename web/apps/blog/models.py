from django.db import models
from tinymce.models import HTMLField
from users.models import Author
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=5)
    description = models.TextField()
    content = HTMLField()
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="blog_posts", blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    read_time = models.IntegerField()
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
