"""ferias URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('website.urls'), name='sitio'),
    path('ferias/', include('marketplaces.urls'), name='ferias'),
    path('productos/', include('products.urls'), name='productos'),
    path('consejos/', include('content.urls'), name='consejos'),
    path('colaboracion/', include('crowdsourcing.urls'), name='crowdsourcing'),
    path('api/', include('api.urls'), name='api'),
    path('usuarios/', include('users.urls'), name='usuarios'),
    path('about/', include('about.urls'), name='about'),
    path('blog/', include('blog.urls'), name='blog'),
]
