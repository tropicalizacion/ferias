from django.urls import path

from . import views

urlpatterns = [
    path('', views.sugerencias, name='sugerencias'),
    path('gracias/', views.sugerencias_gracias, name='sugerencias_gracias'),
    path('ferias/', views.sugerencias_ferias, name='sugerencias_ferias'),
    path('productos/', views.sugerencias_productos, name='sugerencias_productos'),
    path('ferias/<marketplace_url>/', views.sugerencias_feria, name='sugerencias_feria'),
    path('ferias/<marketplace_url>/productos/', views.sugerencias_feria_productos, name='sugerencias_feria_productos'),
    path('productos/<product_url>/', views.sugerencias_producto, name='sugerencias_producto'),
    path('revisiones/', views.revisiones, name='revisiones'),
    path('revisiones/ferias/', views.revisiones_ferias, name='revisiones_ferias'),
    path('revisiones/productos/', views.revisiones_productos, name='revisiones_productos'),
    path('revisiones/ferias/<marketplace_url>/', views.revisiones_feria, name='revisiones_feria'),
    path('revisiones/productos/<product_url>/', views.revisiones_producto, name='revisiones_producto'),
]