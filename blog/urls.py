from django.urls import path

from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path("crear", views.create_post, name="create_post"),
    path("<slug:slug>/", views.post, name="post"),
]