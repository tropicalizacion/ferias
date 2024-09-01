from django.shortcuts import render
from django.http import FileResponse
from rest_framework import viewsets
from marketplaces.models import Marketplace
from .serializers import MarketplaceSerializer
from .serializers import GeoMarketplaceSerializer
from website.models import Text

import pandas as pd
from django.http import FileResponse
import io
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from django.conf import settings

# Create your views here.


@extend_schema_view(
    list=extend_schema(
        summary="Listar todas las ferias",
        description="Este endpoint devuelve una lista de todas las ferias disponibles en la plataforma.",
        responses={200: MarketplaceSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Crear una nueva feria",
        description="Este endpoint permite crear una nueva feria en la plataforma.",
        responses={201: MarketplaceSerializer},
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de una feria específica",
        description="Este endpoint devuelve los detalles de una feria dada su URL.",
        responses={200: MarketplaceSerializer},
    ),
    update=extend_schema(
        summary="Actualizar la información de una feria",
        description="Este endpoint permite ingresar información más actualizada acerca de una feria específica, dada su URL y su nombre. Este endpoint requiere enviar los datos de todos los atributos de dicha feria.",
        responses={200: MarketplaceSerializer},
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente la información de una feria",
        description="Este endpoint permite ingresar información más actualizada acerca de una feria específica dada su URL y su nombre, sin necesidad de enviar los datos de todos los atributos de dicha feria, sino sólo aquellos datos que se vayan a actualizar.",
        responses={200: MarketplaceSerializer},
    ),
    destroy=extend_schema(
        summary="Eliminar una feria específica",
        description="Este endpoint permite eliminar la información de una feria dada su URL.",
        responses={204: MarketplaceSerializer},
    ),
)
class MarketplaceViewSet(viewsets.ModelViewSet):
    queryset = Marketplace.objects.all().order_by("name")
    serializer_class = MarketplaceSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Listar todas las ubicaciones de las ferias",
        description="Este endpoint devuelve una lista de todas las ubicaciones de las ferias disponibles en la plataforma.",
        responses={200: MarketplaceSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Crear una nueva ubicación de feria",
        description="Este endpoint permite crear una nueva ubicaciones de una feria en la plataforma.",
        responses={201: MarketplaceSerializer},
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de la ubicación de una feria específica",
        description="Este endpoint devuelve los detalles ubicación de una feria dada su URL.",
        responses={200: MarketplaceSerializer},
    ),
    update=extend_schema(
        summary="Actualizar la ubicación de una feria",
        description="Este endpoint permite ingresar información más actualizada acerca de la ubicación una feria específica, dada su URL y su nombre. Este endpoint requiere enviar los datos de todos los atributos de dicha feria.",
        responses={200: MarketplaceSerializer},
    ),
    partial_update=extend_schema(
        summary="Actualizar la ubicación de una feria",
        description="Este endpoint permite ingresar información más actualizada acerca de la ubicación de una feria específica dada su URL y su nombre, sin necesidad de enviar los datos de todos los atributos de dicha feria, sino sólo aquellos datos que se vayan a actualizar.",
        responses={200: MarketplaceSerializer},
    ),
    destroy=extend_schema(
        summary="Eliminar la ubicación de una feria específica",
        description="Este endpoint permite eliminar la ubicación de una feria dada su URL.",
        responses={204: MarketplaceSerializer},
    ),
)
class GeoMarketplaceViewSet(viewsets.ModelViewSet):
    queryset = Marketplace.objects.all().order_by("name")
    serializer_class = GeoMarketplaceSerializer

def get_schema(request):
    file_path = settings.BASE_DIR / "api" / "schema.yml"
    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="schema.yml"
    )


def datos(request):
    text = Text.objects.filter(page="/datos")
    texts = {}
    texts["hero"] = text.filter(section="hero").first()
    texts["hero_desc"] = text.filter(section="hero_desc").first()

    context = {
        "texts": texts,
    }
    return render(request, "datos.html", context)


def ferias(request):
    ferias = Marketplace.objects.all().order_by("name")
    df = pd.DataFrame.from_records(ferias.values())
    if "formato" in request.GET:
        if request.GET["formato"] == "csv":
            df.to_csv("ferias.csv", index=False)
            return FileResponse(
                open("ferias.csv", "rb"), as_attachment=True, filename="ferias.csv"
            )
        elif request.GET["formato"] == "excel":
            df.to_excel("ferias.xlsx", index=False)
            return FileResponse(
                open("ferias.xlsx", "rb"), as_attachment=True, filename="ferias.xlsx"
            )


def productos(request):
    return FileResponse(open("productos.csv", "rb"))
