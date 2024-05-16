from django.urls import path

from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("eventos/", views.events, name="events"),
    path("noticias/", views.newss, name="newss"),
    path("alertas/", views.alerts, name="alerts"),
    path("eventos/crear", views.create_event, name="create_event"),
    path("noticias/crear", views.create_news, name="create_news"),
    path("alertas/crear", views.create_alert, name="create_alert"),
    path("eventos/<slug:event_slug>/", views.event, name="event"),
    path("noticias/<slug:news_slug>/", views.news, name="news"),
    path("alertas/<slug:alert_slug>/", views.alert, name="alert"),
]
