from django.shortcuts import render
from marketplaces.models import Marketplace
from .models import MarketplaceEdit, PhotoEdit, OpeningHoursEdit, ContactEdit
import osm_opening_hours_humanized as hoh
from django.contrib.auth.decorators import login_required

# Create your views here.


def sugerencias(request):
    marketplaces = Marketplace.objects.all()
    context = {"marketplaces": marketplaces}
    return render(request, "sugerencias.html", context)


def sugerencias_ferias(request):
    return render(request, "sugerencias_ferias.html")


def sugerencias_productos(request):
    return render(request, "sugerencias_productos.html")


def sugerencias_feria(request, marketplace_url):
    
    if request.method == "POST":
        marketplace = Marketplace.objects.get(marketplace_url=marketplace_url)
        print(f"\nPost:\n{request.POST}\n")
        
        # Create the marketplace edit object
        marketplace_edit = MarketplaceEdit()

        # General information
        marketplace_edit.marketplace = marketplace
        if request.POST.get("name") != "":
            marketplace_edit.name = request.POST.get("name")
        if request.POST.get("name_alternate") != "":
            marketplace_edit.name_alternate = request.POST.get("name_alternate")
        if request.POST.get("operator") != "":
            marketplace_edit.operator = request.POST.get("operator")
        if request.POST.get("description") != "":
            marketplace_edit.description = request.POST.get("description")
        if request.POST.get("address") != "":
            marketplace_edit.address = request.POST.get("address")
        if request.POST.get("size") != "size_unknown":
            marketplace_edit.size = request.POST.get("size")
        if request.POST.get("opening_date") != "":
            marketplace_edit.opening_date = request.POST.get("opening_date")
        
        # Infrastructure
        marketplace_edit.fairground = request.POST.get("fairground")
        marketplace_edit.indoor = request.POST.get("indoor")
        marketplace_edit.toilets = request.POST.get("toilets")
        marketplace_edit.handwashing = request.POST.get("handwashing")
        marketplace_edit.drinking_water = request.POST.get("drinking_water")
        marketplace_edit.parking = request.POST.get("parking")
        marketplace_edit.bicycle_parking = request.POST.get("bicycle_parking")
        
        # Services
        marketplace_edit.food = request.POST.get("food")
        marketplace_edit.drinks = request.POST.get("drinks")
        marketplace_edit.handicrafts = request.POST.get("handicrafts")
        marketplace_edit.butcher = request.POST.get("butcher")
        marketplace_edit.dairy = request.POST.get("dairy")
        marketplace_edit.seafood = request.POST.get("seafood")
        marketplace_edit.garden_centre = request.POST.get("garden_centre")
        marketplace_edit.florist = request.POST.get("florist")

        # Submitted by
        marketplace_edit.submitted_by = request.POST.get("submitted_by")

        # Save the marketplace edit object
        marketplace_edit.save()

        # Save the phones, emails and websites in the contact edit table
        i = 1
        go = (
            ((f"phone_{i}" in request.POST) and (request.POST.get(f"phone_{i}") != ""))
            or ((f"email_{i}" in request.POST) and (request.POST.get(f"email_{i}") != ""))
            or ((f"link_{i}" in request.POST) and (request.POST.get(f"link_{i}") != ""))
        )
        while go:
            if f"phone_{i}" in request.POST:
                phone = request.POST.get(f"phone_{i}")
            else:
                phone = None
            if f"email_{i}" in request.POST:
                email = request.POST.get(f"email_{i}")
            else:
                email = None
            if f"link_{i}" in request.POST:
                website = request.POST.get(f"link_{i}")
            else:
                website = None
            contact_edit = ContactEdit(
                marketplace=marketplace,
                marketplace_edit_id=marketplace_edit,
                phone=phone,
                email=email,
                website=website,
            )
            contact_edit.save()
            i += 1
            go = (
                (f"phone_{i}" in request.POST)
                or (f"email_{i}" in request.POST)
                or (f"link_{i}" in request.POST)
            )

        # Save the opening hours in the opening hours edit table
        i = 1
        go = (
            (f"day_opens_{i}" in request.POST)
            and (f"hour_opens_{i}" in request.POST)
            and (f"hour_closes_{i}" in request.POST)
        )
        while go:
            if f"day_opens_{i}" in request.POST:
                day_opens = request.POST.get(f"day_opens_{i}")
                print(f"day_opens_{i}: {day_opens}")
            else:
                day_opens = None
            if f"hour_opens_{i}" in request.POST:
                hour_opens = request.POST.get(f"hour_opens_{i}")
            else:
                hour_opens = None
            if f"hour_closes_{i}" in request.POST:
                hour_closes = request.POST.get(f"hour_closes_{i}")
            else:
                hour_closes = None
            opening_hours_edit = OpeningHoursEdit(
                marketplace=marketplace,
                marketplace_edit_id=marketplace_edit,
                day_opens=day_opens,
                hour_opens=hour_opens,
                day_closes=day_opens,
                hour_closes=hour_closes,
            )
            opening_hours_edit.save()
            i += 1
            go = (
                (f"day_opens_{i}" in request.POST)
                and (f"hour_opens_{i}" in request.POST)
                and (f"hour_closes_{i}" in request.POST)
            )

        context = {"marketplace": marketplace}

        return render(request, "sugerencias_gracias.html", context)

    else:
        marketplace = Marketplace.objects.get(marketplace_url=marketplace_url)
        size_choices = marketplace.SIZE_CHOICES
        opening_hours_edit = OpeningHoursEdit()

        schedule = None
        if marketplace.opening_hours:
            schedule_object = hoh.OHParser(marketplace.opening_hours, locale="en")
            schedule = schedule_object.description()
            print(schedule)

        context = {
            "marketplace": marketplace,
            "size_choices": size_choices,
            "schedule": schedule,
        }
        return render(request, "sugerencias_feria.html", context)


def sugerencias_producto(request, product_url):
    return render(request, "sugerencias_producto.html")


def revisiones_ferias(request):
    return render(request, "revisiones_ferias.html")


def revisiones_productos(request):
    return render(request, "revisiones_productos.html")


def revisiones_feria(request, marketplace_url):
    return render(request, "revisiones_feria.html")


def revisiones_producto(request, product_url):
    return render(request, "revisiones_producto.html")
