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
from django.conf.urls.static import static
from django.conf import settings
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('website.urls'), name='sitio'),
    path('ferias/', include('marketplaces.urls'), name='ferias'),
    path('productos/', include('products.urls'), name='productos'),
    path('consejos/', include('content.urls'), name='consejos'),
    path('avisos/', include('feed.urls'), name='avisos'),
    path('blog/', include('blog.urls'), name='blog'),
    path('sugerencias/', include('crowdsourcing.urls'), name='sugerencias'),
    path('datos/', include('api.urls'), name='api'),
    path('usuarios/', include('users.urls'), name='usuarios'),
    path('recetas/', include('recipes.urls'), name='recetas'),
    path('cms/', include(wagtailadmin_urls)),     # Panel de administración de Wagtail
    path('documents/', include(wagtaildocs_urls)),  # Descarga de documentos
    path('paginas/', include(wagtail_urls)),  # Rutas públicas manejadas por Wagtail

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
