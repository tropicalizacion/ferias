from django.urls import path

from . import views

urlpatterns = [
    path('', views.sugerencias, name='colaboracion'),
    path('<marketplace_url>/', views.sugerencia, name='sugerencia'),
    path('revision/', views.revisiones, name='revisiones'),
    path('revision/<marketplace_url>/', views.revision, name='revision'),
]