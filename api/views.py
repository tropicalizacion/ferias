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

# Create your views here.


class MarketplaceViewSet(viewsets.ModelViewSet):
    queryset = Marketplace.objects.all().order_by("name")
    serializer_class = MarketplaceSerializer

class GeoMarketplaceViewSet(viewsets.ModelViewSet):
    queryset = Marketplace.objects.all().order_by("name")
    serializer_class = GeoMarketplaceSerializer


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
