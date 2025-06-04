# Django imports
from django.urls import path, include

# DRF imports
from rest_framework import routers
from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS

# DRF Spectacular imports
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

# local imports
from . import views


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

router = routers.DefaultRouter()
router.register(r"ferias", views.MarketplaceViewSet)
router.register(r"geoferias", views.GeoMarketplaceViewSet, basename="geo_marketplace")
router.register(r"productos", views.ProductViewSet)

# To see the api documentation, go to /api/docs/. 
# If you are creating a new API or endpoint, in order for the documentation to 
# be generated, read the instrucctions in the `comb_schema_script.py` file.

urlpatterns = [
    path("", views.datos, name="datos"),
    path("ferias", views.ferias, name="datos-ferias"),
    path("productos", views.productos, name="datos-productos"),
    path("api/docs/schema/", views.get_schema, name="schema"),
    path("api/docs/", SpectacularRedocView.as_view(url_name='schema' , 
                                                   permission_classes=[IsAdminUser | ReadOnly]), 
                                                   name="docs"),
    path("api/", include(router.urls)),
]
