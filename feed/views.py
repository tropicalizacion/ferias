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
