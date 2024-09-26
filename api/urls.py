from django.urls import path, include
from rest_framework import routers
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

router = routers.DefaultRouter()
router.register(r"ferias", views.MarketplaceViewSet)
router.register(r"geoferias", views.GeoMarketplaceViewSet, basename="geo_marketplace")

urlpatterns = [
    path("", views.datos, name="datos"),
    path("ferias", views.ferias, name="datos-ferias"),
    path("productos", views.productos, name="datos-productos"),
    path("api/docs/schema/", views.get_schema, name="schema"),
    path("api/docs/", SpectacularRedocView.as_view(url_name='schema'), name="docs"),
    path("api/", include(router.urls)),
]
