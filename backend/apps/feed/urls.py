from django.urls import path

from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("eventos/crear", views.create_event, name="create_event"),
    path("noticias/crear", views.create_news, name="create_news"),
    path("alertas/crear", views.create_alert, name="create_alert"),
    path("eventos/<slug:event_slug>/<int:id>", views.event, name="event"),
    path("noticias/<slug:news_slug>/<int:id>", views.news, name="news"),
    path("alertas/<slug:alert_slug>/<int:id>", views.alert, name="alert"),
]
