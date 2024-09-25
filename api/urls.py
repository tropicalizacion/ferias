from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"ferias", views.MarketplaceViewSet)
router.register(r"geoferias", views.GeoMarketplaceViewSet, basename="geo_marketplace")

urlpatterns = [
    path("", views.datos, name="datos"),
    path("ferias", views.ferias, name="datos-ferias"),
    path("productos", views.productos, name="datos-productos"),
    path("api/", include(router.urls)),
]
