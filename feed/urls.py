from django.urls import path

from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("eventos/", views.feed, name="feed"),
    path("noticias/", views.feed, name="feed"),
    path("alertas/", views.feed, name="feed"),
    path("eventos/<slug:event_slug>/", views.event, name="feed"),
    path("noticias/<slug:news_slug>/", views.news, name="feed"),
    path("alertas/<slug:alert_slug>/", views.alert, name="feed"),
]
