from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Tag
from users.models import Author
from django.contrib.auth.decorators import login_required

def blog(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'blog_posts': blog_posts})

@login_required
def create_post(request):
    user = request.user
    if user.is_authenticated:
        
        if request.method == 'POST':
            author = Author.objects.get(user=request.user)
            title = request.POST.get('title')
            description = request.POST.get('description')
            content = request.POST.get('content')
            image = request.FILES.get('image')
            read_time = request.POST.get('read_time')
            tags_ids = request.POST.getlist('tags')

            post = BlogPost(
                title=title,
                author=author,
                description=description,
                content=content,
                image=image,
                read_time=read_time
            )
            post.save()

            post.tags.set(tags_ids)
            
            return redirect('blog')
        
        tags = Tag.objects.all()
        return render(request, "create_post.html", {'tags': tags})


def post(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    
    return render(request, 'post.html', {'post': blog_post})
