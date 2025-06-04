# Standart library imports
from io import BytesIO
from zipfile import ZipFile

# Third party imports
import pandas as pd
import geopandas as gpd
from shapely import Point

# Django imports
from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings

# DRF imports
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, BasePermission

# drf_spectacular imports
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

# Models imports
from marketplaces.models import Marketplace
from products.models import Product, Variety
from website.models import Text

# Serializers imports
from .serializers import (
    MarketplaceSerializer,
    GeoMarketplaceSerializer,
    ProductSerializer,
    VarietySerializer,
)



# Create your views here.
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


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
        description="Este endpoint permite ingresar información más actualizada acerca de una feria específica, dada su URL. Este endpoint requiere enviar los datos completos de todos los atributos de dicha feria.",
        responses={200: MarketplaceSerializer},
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente la información de una feria",
        description="Este endpoint permite ingresar información más actualizada acerca de una feria específica, dada su URL, sin necesidad de enviar los datos de todos los atributos de dicha feria, sino sólo aquellos datos que se vayan a actualizar.",
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
    permission_classes = [IsAdminUser | ReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="Listar todas las ubicaciones de las ferias",
        description="Este endpoint devuelve una lista de todas las ubicaciones de las ferias disponibles en la plataforma.",
        responses={200: MarketplaceSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Crear una nueva ubicación de feria",
        description="Este endpoint permite crear una nueva ubicación de una feria en la plataforma.",
        responses={201: MarketplaceSerializer},
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de la ubicación de una feria específica",
        description="Este endpoint devuelve los detalles de la ubicación de una feria dada su URL.",
        responses={200: MarketplaceSerializer},
    ),
    update=extend_schema(
        summary="Actualizar la ubicación de una feria",
        description="Este endpoint permite ingresar información más actualizada acerca de la ubicación de una feria específica, dada su URL. Este endpoint requiere enviar los datos completos de todos los atributos de dicha ubicación.",
        responses={200: MarketplaceSerializer},
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente la ubicación de una feria",
        description="Este endpoint permite ingresar información más actualizada acerca de la ubicación de una feria específica, dada su URL, sin necesidad de enviar los datos de todos los atributos de dicha ubicación, sino sólo aquellos datos que se vayan a actualizar.",
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
    permission_classes = [IsAdminUser | ReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="Listar todos los productos de las ferias",
        description="Este endpoint devuelve una lista de todos los productos disponibles de las ferias.",
        responses={200: ProductSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Crear un nuevo producto",
        description="Este endpoint permite crear un nuevo producto de una feria en la plataforma.",
        responses={201: ProductSerializer},
    ),
    retrieve=extend_schema(
        summary="Obtener detalles de un producto específico",
        description="Este endpoint devuelve los detalles de un producto dada su URL.",
        responses={200: ProductSerializer},
    ),
    update=extend_schema(
        summary="Actualizar el producto de una feria",
        description="Este endpoint permite ingresar información más actualizada acerca de un producto, dada su URL. Este endpoint requiere enviar los datos completos de todos los atributos de dicho producto.",
        responses={200: ProductSerializer},
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente el producto de una feria",
        description="Este endpoint permite ingresar información más actualizada acerca de un producto, dada su URL, sin necesidad de enviar los datos de todos los atributos de dicho producto, sino sólo aquellos datos que se vayan a actualizar.",
        responses={200: ProductSerializer},
    ),
    destroy=extend_schema(
        summary="Eliminar un producto específico",
        description="Este endpoint permite eliminar un producto dado su URL.",
        responses={204: ProductSerializer},
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("varieties").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser | ReadOnly]


def get_schema(request):
    file_path = settings.BASE_DIR / "api" / "schema.yml"
    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="schema.yml"
    )


# class VarietyViewSet(viewsets.ModelViewSet):
#     queryset = Variety.objects.all().order_by("scientific_name")
#     serializer_class = VarietySerializer


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
        elif request.GET["formato"] == "geojson":

            def format_points(value):
                return Point(value)

            df["geometry"] = df["location"].apply(format_points)

            gdf = gpd.GeoDataFrame(
                df[
                    ["name", "province", "canton", "district", "postal_code", "address"]
                ],
                geometry=df["geometry"],
                crs="EPSG:4326",
            )
            gdf.to_file("ferias.geojson", driver="GeoJSON")
            return FileResponse(
                open("ferias.geojson", "rb"),
                as_attachment=True,
                filename="ferias.geojson",
            )


def productos(request):
    # Create dataframe for productos
    productos = Product.objects.all().order_by("common_name")
    productos_df = pd.DataFrame.from_records(productos.values())
    productos_df.drop("icon", axis=1, inplace=True)

    # Create dataframe for variedades
    variedades = Variety.objects.all().order_by("variety_id")
    variedades_df = pd.DataFrame.from_records(variedades.values())
    variedades_df.drop("image", axis=1, inplace=True)

    if "formato" in request.GET:
        if request.GET["formato"] == "csv":
            # productos_df.to_csv("productos.csv", index=False)
            # variedades_df.to_csv("variedades.csv", index=False)

            # Create a zip file response
            zip_buffer = BytesIO()
            with ZipFile(zip_buffer, "w") as zip_file:
                # Safe productos csv in the zip file
                csv_buffer1 = BytesIO()
                productos_df.to_csv(csv_buffer1, index=False)
                zip_file.writestr("productos.csv", csv_buffer1.getvalue())

                # GSafe variedades csv in the zip file
                csv_buffer2 = BytesIO()
                variedades_df.to_csv(csv_buffer2, index=False)
                zip_file.writestr("variedades.csv", csv_buffer2.getvalue())

            zip_buffer.seek(0)
            return FileResponse(
                zip_buffer, as_attachment=True, filename="productos.zip"
            )

        elif request.GET["formato"] == "excel":
            excel_buffer = BytesIO()
            # to save the file locally
            file_path = "productos.xlsx"

            # Save dataframes in the same excel file
            # replace excel_buffer with file_path to save the file locally
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                productos_df.to_excel(writer, sheet_name="Productos", index=False)
                variedades_df.to_excel(writer, sheet_name="Variedades", index=False)

            excel_buffer.seek(0)

            # return FileResponse(
            #     open(file_path, "rb"), as_attachment=True, filename="productos.xlsx"
            # )
            return FileResponse(
                excel_buffer, as_attachment=True, filename="Productos.xlsx"
            )
        elif request.GET["formato"] == "json":
            # use the serializer to create the json file
            productos = Product.objects.all().order_by("common_name")
            serializer = ProductSerializer(productos, many=True)
            json_data = JSONRenderer().render(
                serializer.data, renderer_context={"indent": 4}
            )

            # save the json file locally
            with open("productos.json", "wb") as json_file:
                json_file.write(json_data)

            return FileResponse(
                open("productos.json", "rb"),
                as_attachment=True,
                filename="productos.json",
            )
