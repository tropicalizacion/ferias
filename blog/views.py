from django.shortcuts import render
from .models import BlogPost
# Create your views here.

def blog(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'blog_posts': blog_posts})