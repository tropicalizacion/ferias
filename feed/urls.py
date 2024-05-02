from django.urls import path

from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("eventos/", views.feed, name="feed"),
    path("noticias/", views.feed, name="feed"),
    path("alertas/", views.feed, name="feed"),
    path("eventos/crear", views.create_event, name="create_event"),
    path("noticias/crear", views.create_news, name="create_news"),
    path("alertas/crear", views.create_alert, name="create_alert"),
    path("eventos/<slug:event_slug>/", views.event, name="feed"),
    path("noticias/<slug:news_slug>/", views.news, name="feed"),
    path("alertas/<slug:alert_slug>/", views.alert, name="feed"),
]
