from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]