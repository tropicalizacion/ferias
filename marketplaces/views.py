from django.shortcuts import render, get_object_or_404
from .models import Marketplace
from website.models import Announcement, Text
from feed.models import Event
import humanized_opening_hours as hoh
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
import math
import json
import jsonpickle
from datetime import datetime


def get_structured_data(marketplace):
    # TODO: Revisar dónde colocar todo esto.
    structured_data = {
        "@context": "http://schema.org/",
        "@type": "LocalBusiness",
        "name": marketplace.name,
        "telephone": marketplace.phone,
        "email": marketplace.email,
        "image": "",  # TODO: Revisar modelo Photo/ImageObject para incluir imagen y texto alternativo.
        "address": get_structured_address(marketplace),
        "geo": get_structured_geo(marketplace),
        "url": [
            f"https://deferia.cr/ferias/{marketplace.name.lower()}/",
            marketplace.facebook,
            marketplace.instagram,
            marketplace.website,
        ],
        "openingHoursSpecification": get_structured_opening_hours(marketplace),
        # "nearestMarketplaces": get_structured_closest_marketplaces(marketplace), # TODO: Revisar esta propiedad adicional.
        "makesOffer": get_structured_infrastructure(marketplace)
        + get_structured_services(marketplace),
        "event": get_structured_events(marketplace),
        "parentOrganization": marketplace.operator,
        "priceRange": "$",
        "paymentAccepted": "",  # TODO: marketplace.payment ManyToMany.
        "currenciesAccepted": "CRC",
        "publicAccess": True,
    }

    return structured_data


def get_structured_services(marketplace):
    services = (
        Marketplace.objects.values(
            "food",
            "drinks",
            "handicrafts",
            "butcher",
            "dairy",
            "seafood",
            "spices",
            "garden_centre",
            "florist",
        )
        .filter(pk=marketplace.marketplace_url)
        .first()
    )
    structured_services = []

    for key, value in services.items():
        if value:
            service = {
                "@type": "Offer",
                "name": key.replace("_", " ").title(),
                "category": "Service",
                "description": "Available",
            }

            structured_services.append(service)

    return structured_services


def get_structured_infrastructure(marketplace):
    infrastructure = (
        Marketplace.objects.values(
            "parking",
            "bicycle_parking",
            "fairground",
            "indoor",
            "toilets",
            "handwashing",
            "drinking_water",
        )
        .filter(pk=marketplace.marketplace_url)
        .first()
    )
    structured_infrastructure = []

    for key, value in infrastructure.items():
        if value:
            infrastructure = {
                "@type": "Offer",
                "name": key.replace("_", " ").title(),
                "category": "Infrastructure",
                "description": "Available",
            }

            structured_infrastructure.append(infrastructure)

    return structured_infrastructure


def get_structured_closest_marketplaces(marketplace):
    closest_marketplaces = (
        Marketplace.objects.annotate(
            distance=Distance("location", marketplace.location)
        )
        .exclude(pk=marketplace.marketplace_url)
        .order_by("distance")[0:3]
    )
    structured_marketplaces = []

    for closest_marketplace in closest_marketplaces:
        closest_marketplace.distance = round(closest_marketplace.distance.km, 1)

        structured_marketplace = get_structured_data(closest_marketplace)
        structured_marketplaces.append(structured_marketplace)

    return structured_marketplaces


def get_structured_geo(marketplace):
    geo_coordinates = {
        "@type": "GeoCoordinates",
        "latitude": marketplace.location.y,
        "longitude": marketplace.location.x,
    }

    return geo_coordinates


def get_structured_opening_hours(marketplace):
    days_mapping = {
        "Mo": "Monday",
        "Tu": "Tuesday",
        "We": "Wednesday",
        "Th": "Thursday",
        "Fr": "Friday",
        "Sa": "Saturday",
        "Su": "Sunday",
    }

    schedule_list = marketplace.opening_hours.split("; ")
    opening_hours = []

    for entry in schedule_list:
        day, time_range = entry.split(" ")
        start_time, end_time = time_range.split("-")

        start_time = datetime.strptime(start_time, "%H:%M").strftime("%H:%M")
        end_time = datetime.strptime(end_time, "%H:%M").strftime("%H:%M")

        specification = {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": days_mapping[day],
            "opens": start_time,
            "closes": end_time,
        }

        opening_hours.append(specification)

    return opening_hours


def get_structured_events(marketplace):
    events = Event.objects.filter(marketplace=marketplace).order_by("-start_date")
    structured_events = []

    for event in events:
        structured_event = {
            "@type": "Event",
            "name": event.name,
            "description": event.description,
        }
        structured_events.append(structured_event)

    return structured_events


def get_structured_address(marketplace):
    address = {
        "@type": "PostalAddress",
        "streetAddress": marketplace.address,
        "addressLocality": marketplace.district,
        "addressRegion": marketplace.province,
        "addressCountry": "CR",
        "postalCode": marketplace.postal_code,
    }

    return address


# Create your views here.


def ferias(request):
    """View function for all ferias page of site."""

    marketplaces = Marketplace.objects.all().order_by("name")
    texts = Text.objects.filter(page="/ferias")

    total_marketplaces = marketplaces.count()
    n_sanjose = marketplaces.filter(province="San José").count()
    n_alajuela = marketplaces.filter(province="Alajuela").count()
    n_cartago = marketplaces.filter(province="Cartago").count()
    n_heredia = marketplaces.filter(province="Heredia").count()
    n_guanacaste = marketplaces.filter(province="Guanacaste").count()
    n_puntarenas = marketplaces.filter(province="Puntarenas").count()
    n_limon = marketplaces.filter(province="Limón").count()
    n_provinces = [
        n_sanjose,
        n_alajuela,
        n_cartago,
        n_heredia,
        n_guanacaste,
        n_puntarenas,
        n_limon,
    ]
    n_monday = marketplaces.filter(opening_hours__contains="Mo").count()
    n_tuesday = marketplaces.filter(opening_hours__contains="Tu").count()
    n_wednesday = marketplaces.filter(opening_hours__contains="We").count()
    n_thursday = marketplaces.filter(opening_hours__contains="Th").count()
    n_friday = marketplaces.filter(opening_hours__contains="Fr").count()
    n_saturday = marketplaces.filter(opening_hours__contains="Sa").count()
    n_sunday = marketplaces.filter(opening_hours__contains="Su").count()
    n_days = [
        n_monday,
        n_tuesday,
        n_wednesday,
        n_thursday,
        n_friday,
        n_saturday,
        n_sunday,
    ]
    n_fairground = (
        marketplaces.filter(fairground=True).count() / total_marketplaces * 100
    )
    n_indoor = marketplaces.filter(indoor=True).count() / total_marketplaces * 100
    n_parking = (
        marketplaces.filter(parking="surface").count() / total_marketplaces * 100
    )
    n_infrastructure = [n_fairground, n_indoor, n_parking]
    n_infrastructure = [math.ceil(i) for i in n_infrastructure]
    n_food = marketplaces.filter(food=True).count() / total_marketplaces * 100
    n_drinks = marketplaces.filter(drinks=True).count() / total_marketplaces * 100
    n_handicrafts = (
        marketplaces.filter(handicrafts=True).count() / total_marketplaces * 100
    )
    n_butcher = marketplaces.filter(butcher=True).count() / total_marketplaces * 100
    n_dairy = marketplaces.filter(dairy=True).count() / total_marketplaces * 100
    n_seafood = marketplaces.filter(seafood=True).count() / total_marketplaces * 100
    n_garden_centre = (
        marketplaces.filter(garden_centre=True).count() / total_marketplaces * 100
    )
    n_florist = marketplaces.filter(florist=True).count() / total_marketplaces * 100
    n_amenities = [
        n_food,
        n_drinks,
        n_handicrafts,
        n_butcher,
        n_dairy,
        n_seafood,
        n_garden_centre,
        n_florist,
    ]
    n_amenities = [math.ceil(i) for i in n_amenities]

    text = Text.objects.filter(page="/ferias")
    texts = {}
    texts["hero"] = text.filter(section="hero").first()
    texts["ubicacion"] = text.filter(section="ubicacion").first()
    texts["features_saludable"] = text.filter(section="features_saludable").first()
    texts["numeros"] = text.filter(section="numeros").first()
    texts["buscador"] = text.filter(section="buscador").first()
    texts["lista"] = text.filter(section="lista").first()

    marketplaces_map = []
    for marketplace in marketplaces:
        try:
            marketplace_dict = {}
            marketplace_dict["name"] = marketplace.name
            marketplace_dict["latitude"] = marketplace.location.y
            marketplace_dict["longitude"] = marketplace.location.x
            marketplaces_map.append(marketplace_dict)
        except:
            pass
    marketplaces_map = json.dumps(marketplaces_map)

    context = {
        "texts": texts,
        "marketplaces": marketplaces,
        "marketplaces_map": marketplaces_map,
        "total_marketplaces": total_marketplaces,
        "n_provinces": n_provinces,
        "n_days": n_days,
        "n_infrastructure": n_infrastructure,
        "n_amenities": n_amenities,
    }

    if request.method == "POST":
        (
            marketplaces_match,
            marketplaces_others,
            marketplaces_keyword,
            keyword,
            query_text,
            by_location,
        ) = search_marketplaces(request.POST)
        context["show_results"] = True
        context["query_text"] = query_text
        context["by_location"] = by_location
        context["keyword"] = keyword
        context["marketplaces_match"] = marketplaces_match
        context["marketplaces_others"] = marketplaces_others
        context["marketplaces_keyword"] = marketplaces_keyword

    return render(request, "ferias.html", context)


def feria(request, marketplace_url):
    """View function for every feria page of site."""

    today = datetime.today()

    marketplace = get_object_or_404(Marketplace, pk=marketplace_url)
    closest_marketplaces = (
        Marketplace.objects.annotate(
            distance=Distance("location", marketplace.location)
        )
        .exclude(pk=marketplace_url)
        .order_by("distance")[0:3]
    )
    for closest_marketplace in closest_marketplaces:
        closest_marketplace.distance = round(closest_marketplace.distance.km, 1)

    opening_hours = marketplace.opening_hours
    is_open = None
    description = None
    opens_in = None
    closes_in = None
    if opening_hours != "":
        try:
            oh = hoh.OHParser(opening_hours)
            is_open = oh.is_open()
            if is_open:
                closes_in = oh.render().time_before_next_change(word=False)
                closes_in = (
                    closes_in.replace("days", "días")
                    .replace("day", "día")
                    .replace("hours", "horas")
                    .replace("hour", "hora")
                    .replace("minutes", "minutos")
                    .replace("minute", "minuto")
                    .replace("seconds", "segundos")
                    .replace("second", "segundo")
                )
            else:
                opens_in = oh.render().time_before_next_change(word=False)
                opens_in = (
                    opens_in.replace("days", "días")
                    .replace("day", "día")
                    .replace("hours", "horas")
                    .replace("hour", "hora")
                    .replace("minutes", "minutos")
                    .replace("minute", "minuto")
                    .replace("seconds", "segundos")
                    .replace("second", "segundo")
                )
            description = oh.render().full_description()
            for i, _ in enumerate(description):
                description[i] = (
                    description[i]
                    .replace("Monday", "Lunes")
                    .replace("Tuesday", "Martes")
                    .replace("Wednesday", "Miércoles")
                    .replace("Thursday", "Jueves")
                    .replace("Friday", "Viernes")
                    .replace("Saturday", "Sábado")
                    .replace("Sunday", "Domingo")
                    .replace(": ", ", de ")
                    .replace("to", "a")
                )
        except:
            pass

    infrastructure = {
        "campo ferial": marketplace.fairground,
        "espacio bajo techo": marketplace.indoor,
        "servicios sanitarios": marketplace.toilets,
        "lavamanos": marketplace.handwashing,
        "agua potable": marketplace.drinking_water,
        "estacionamiento de bicicletas": marketplace.bicycle_parking,
    }

    services = {
        "comidas": marketplace.food,
        "bebidas": marketplace.drinks,
        "artesanías": marketplace.handicrafts,
        "carnicería": marketplace.butcher,
        "productos lácteos": marketplace.dairy,
        "pescadería": marketplace.seafood,
        "plantas ornamentales": marketplace.garden_centre,
        "floristería": marketplace.florist,
    }

    events = Event.objects.filter(marketplace=marketplace_url).order_by("-start_date")
    print(f"Evento: {events}")

    announcements = Announcement.objects.filter(marketplace=marketplace_url).order_by(
        "-created"
    )

    text = Text.objects.filter(page="/ferias/feria")
    texts = {}
    texts["servicios_titulo"] = text.filter(section="servicios_titulo").first()
    texts["servicios_descripcion"] = text.filter(
        section="servicios_descripcion"
    ).first()

    # JSON-LD Structured Data
    structured_data = get_structured_data(marketplace)
    serialized_json = jsonpickle.encode(structured_data, unpicklable=False)
    structured_data = jsonpickle.decode(serialized_json)

    context = {
        "marketplace": marketplace,
        "is_open": is_open,
        "opens_in": opens_in,
        "closes_in": closes_in,
        "description": description,
        "closest_marketplaces": closest_marketplaces,
        "infrastructure": infrastructure,
        "services": services,
        "announcements": announcements,
        "events": events,
        "texts": texts,
        "structured_data": structured_data,
    }

    return render(request, "feria.html", context)


def edit(request, marketplace_url):
    return render(request, "edit.html")


def results(request):
    marketplaces = Marketplace.objects.all().order_by("name")
    if request.method == "POST":
        (
            marketplaces_match,
            marketplaces_others,
            marketplaces_keyword,
            keyword,
            query_text,
        ) = search_marketplaces(request.POST)
        context = {
            "show_results": True,
            "marketplaces": marketplaces,
            "marketplaces_match": marketplaces_match,
            "marketplaces_others": marketplaces_others,
            "marketplaces_keyword": marketplaces_keyword,
            "query_text": query_text,
            "keyword": keyword,
        }
        return render(request, "results.html", context)
    else:
        return render(request, "results.html")


def search_marketplaces(submission):
    # Search by location
    location = submission.get("location")
    if location == "any_location":
        marketplaces = Marketplace.objects.all().order_by("name")
        by_location = "any"
    elif location == "my_location":
        longitude = float(submission.get("my_longitude"))
        latitude = float(submission.get("my_latitude"))
        coordinates = Point(longitude, latitude, srid=4326)
        marketplaces = Marketplace.objects.annotate(
            distance=Distance("location", coordinates)
        ).order_by("distance")
        by_location = "my"
    elif location == "some_location":
        longitude = float(submission.get("some_longitude"))
        latitude = float(submission.get("some_latitude"))
        coordinates = Point(longitude, latitude, srid=4326)
        marketplaces = Marketplace.objects.annotate(
            distance=Distance("location", coordinates)
        ).order_by("distance")
        by_location = "some"

    # Search by day of the week
    day = submission.get("day")
    if day != "any_day":
        if day == "today":
            import datetime

            today = datetime.datetime.today().weekday()
            day = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"][today]
            marketplaces = marketplaces.filter(opening_hours__contains=day)
        elif day == "some_day":
            chosen_day = submission.get("choose_day")
            marketplaces = marketplaces.filter(opening_hours__contains=chosen_day)

    # Filter results for exact match
    marketplaces_match = marketplaces

    # Filter by size
    size = submission.get("size")
    if size != "any_size":
        query_size = Q()
        if "size_s" in submission:
            query_size |= Q(size="S")
        if "size_m" in submission:
            query_size |= Q(size="M")
        if "size_l" in submission:
            query_size |= Q(size="L")
        if "size_xl" in submission:
            query_size |= Q(size="XL")
        marketplaces_match = marketplaces_match.filter(query_size)

    # Filter by infrastructure
    query_infrastructure = Q()
    if "fairground" in submission:
        query_infrastructure &= Q(fairground=True)
    if "indoor" in submission:
        query_infrastructure &= Q(indoor=True)
    if "parking" in submission:
        query_infrastructure &= Q(parking="surface")
    marketplaces_match = marketplaces_match.filter(query_infrastructure)

    # Filter by amenities
    query_amenities = Q()
    if "food" in submission:
        query_amenities &= Q(food=True)
    if "drinks" in submission:
        query_amenities &= Q(drinks=True)
    if "handicrafts" in submission:
        query_amenities &= Q(handicrafts=True)
    if "butcher" in submission:
        query_amenities &= Q(butcher=True)
    if "dairy" in submission:
        query_amenities &= Q(dairy=True)
    if "seafood" in submission:
        query_amenities &= Q(seafood=True)
    if "garden_centre" in submission:
        query_amenities &= Q(garden_centre=True)
    if "florist" in submission:
        query_amenities &= Q(florist=True)
    marketplaces_match = marketplaces_match.filter(query_amenities)

    # Filter by keyword
    marketplaces_keyword = None
    keyword = None
    if "keyword" in submission:
        keyword = submission.get("keyword")
        try:
            marketplaces_keyword = marketplaces
            marketplaces_keyword = marketplaces_keyword.filter(
                Q(name__unaccent__trigram_similar=keyword)
                | Q(description__unaccent__trigram_similar=keyword)
            )
        except:
            pass

    # Get other marketplaces

    marketplaces_others = marketplaces.difference(marketplaces_match)
    if by_location != "any":
        marketplaces_others = marketplaces_others.order_by("distance")

    if by_location != "any":
        for marketplace in marketplaces_match:
            marketplace.distance = round(marketplace.distance.km, 1)
        for marketplace in marketplaces_others:
            marketplace.distance = round(marketplace.distance.km, 1)

    # Query text

    query_text = submission.get("query_text")

    return (
        marketplaces_match,
        marketplaces_others,
        marketplaces_keyword,
        keyword,
        query_text,
        by_location,
    )
