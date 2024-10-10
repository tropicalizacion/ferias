from itertools import chain
from operator import attrgetter
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from users.models import MarketplaceAdmin
from feed.models import Alert, Event, News
from marketplaces.models import Marketplace

# Create your views here.


def feed(request):
    
    is_marketplace_admin = False
    user = request.user
    events = Event.objects.all()
    news = News.objects.all()
    alerts = Alert.objects.all()
    
    feed_list = sorted(
        chain(events, news, alerts),
        key=attrgetter('created_at'),
        reverse=True
    )
    
    for item in feed_list:
        item.type_ = type(item).__name__
    
    if user.is_authenticated:
        try:
            marketplace_admin = MarketplaceAdmin.objects.get(user=request.user)
            is_marketplace_admin = True
            
        except MarketplaceAdmin.DoesNotExist:
            is_marketplace_admin = False
    
    context = {
        "is_marketplace_admin": is_marketplace_admin,
        "feed_list": feed_list
    }
    
    return render(request, "feed.html", context)


def event(request, event_slug, id):
    
    event = get_object_or_404(Event, id=id)
    
    return render(request, "event.html", {'event': event})

def events(request):
    return redirect('feed')

def news(request, news_slug, id):
    
    news_item = get_object_or_404(News, id=id)
    
    return render(request, "news.html", {'news_item': news_item})

def newss(request):
    return redirect('feed')

def alert(request, alert_slug, id):
    
    alert = get_object_or_404(Alert, id=id)
    
    return render(request, "alert.html", {'alert': alert})

def alerts(request):
    return redirect('feed')

@login_required
def create_event(request):
    
    user = request.user
    if user.is_authenticated:
        
        try:
            marketplace_admin = MarketplaceAdmin.objects.get(user=request.user)
            
        except MarketplaceAdmin.DoesNotExist:
            print("Este usuario no es un administrador de una feria.")
            return redirect('feed')
        
        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            text = request.POST.get('content')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            location = request.POST.get('location')
            image = request.FILES.get('image')

            event = Event(
                name=name,
                description=description,
                text=text,
                start_date=start_date,
                end_date=end_date,
                location=location,
                image=image,
                marketplace=marketplace_admin.marketplace
            )
            event.save()
            
            return redirect('feed')
        
        context = {
            "marketplace_admin": marketplace_admin,
        }
    
    return render(request, "create_event.html", context)

@login_required
def create_news(request):
    
    user = request.user
    
    if user.is_authenticated:
        try:
            marketplace_admin = MarketplaceAdmin.objects.get(user=request.user)
        except MarketplaceAdmin.DoesNotExist:
            print("Este usuario no es un administrador de una feria.")
            return redirect('feed')

        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            text = request.POST.get('content')
            image = request.FILES.get('image')
            marketplace_admin = MarketplaceAdmin.objects.get(user=request.user)
            marketplace = Marketplace.objects.get(name=marketplace_admin.marketplace)
            
            news = News(
                name=name,
                description=description,
                text=text,
                image=image,
            )
            news.save()
            
            news.marketplaces.add(marketplace)
            
            news.save()

            return redirect('feed')

        context = {
            'marketplace_admin': marketplace_admin,
            'marketplaces': [marketplace_admin.marketplace],
        }
    
    
    return render(request, "create_news.html", context)

@login_required
def create_alert(request):
    
    user = request.user
    
    if user.is_authenticated:
        try:
            marketplace_admin = MarketplaceAdmin.objects.get(user=request.user)
        except MarketplaceAdmin.DoesNotExist:
            print("Este usuario no es un administrador de una feria.")
            return redirect('feed')

        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            text = request.POST.get('content')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            image = request.FILES.get('image')
            marketplace_admin = MarketplaceAdmin.objects.get(user=request.user)
            marketplace = Marketplace.objects.get(name=marketplace_admin.marketplace)

            alert = Alert(
                name=name,
                description=description,
                text=text,
                start_date=start_date,
                end_date=end_date,
                image=image,
            )
            alert.save()
            
            alert.marketplaces.add(marketplace)
            
            alert.save()
            return redirect('feed')

        context = {
            'marketplace_admin': marketplace_admin,
            'marketplaces': [marketplace_admin.marketplace],
        }
    
    return render(request, "create_alert.html", context)
