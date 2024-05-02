from django.shortcuts import render

# Create your views here.


def feed(request):
    return render(request, "feed.html")


def event(request, event_slug):
    return render(request, "event.html")


def news(request, news_slug):
    return render(request, "news.html")


def alert(request, alert_slug):
    return render(request, "alert.html")


def create_event(request):
    return render(request, "create_event.html")


def create_news(request):
    return render(request, "create_news.html")


def create_alert(request):
    return render(request, "create_alert.html")
