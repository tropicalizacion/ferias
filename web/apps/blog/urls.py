from django.urls import path

from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path("crear", views.create_post, name="create_post"),
    path("<slug:slug>/", views.post, name="post"),
    path("<slug:slug>/editar", views.edit_post, name="edit_post"),
    path("eliminar/<int:post_id>/", views.delete_post, name='delete_post')
]