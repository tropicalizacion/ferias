from django.shortcuts import render
from marketplaces.models import Marketplace
from .models import MarketplaceEdit, OpeningHoursEdit, PhoneEdit, EmailEdit, WebsiteEdit
import osm_opening_hours_humanized as hoh
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import ast

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
        marketplace_edit.fairground = ast.literal_eval(request.POST.get("fairground"))
        marketplace_edit.indoor = ast.literal_eval(request.POST.get("indoor"))
        marketplace_edit.toilets = ast.literal_eval(request.POST.get("toilets"))
        marketplace_edit.handwashing = ast.literal_eval(request.POST.get("handwashing"))
        marketplace_edit.drinking_water = ast.literal_eval(request.POST.get("drinking_water"))
        marketplace_edit.parking = ast.literal_eval(request.POST.get("parking"))
        marketplace_edit.bicycle_parking = ast.literal_eval(request.POST.get("bicycle_parking"))
        
        # Services
        marketplace_edit.food = ast.literal_eval(request.POST.get("food"))
        marketplace_edit.drinks = ast.literal_eval(request.POST.get("drinks"))
        marketplace_edit.handicrafts = ast.literal_eval(request.POST.get("handicrafts"))
        marketplace_edit.butcher = ast.literal_eval(request.POST.get("butcher"))
        marketplace_edit.dairy = ast.literal_eval(request.POST.get("dairy"))
        marketplace_edit.seafood = ast.literal_eval(request.POST.get("seafood"))
        marketplace_edit.garden_centre = ast.literal_eval(request.POST.get("garden_centre"))
        marketplace_edit.florist = ast.literal_eval(request.POST.get("florist"))

        # Submitted by
        marketplace_edit.submitted_by = request.POST.get("submitted_by")

        # Save the marketplace edit object
        marketplace_edit.save()

        # Save the phones
        i = 1
        go = f"phone_{i}" in request.POST
        while go:
            phone = request.POST.get(f"phone_{i}")
            phone_edit = PhoneEdit(
                marketplace=marketplace,
                marketplace_edit_id=marketplace_edit,
                phone=phone,
            )
            phone_edit.save()
            i += 1
            go = f"phone_{i}" in request.POST
        
        # Save the emails
        i = 1
        go = f"email_{i}" in request.POST
        while go:
            email = request.POST.get(f"email_{i}")
            email_edit = EmailEdit(
                marketplace=marketplace,
                marketplace_edit_id=marketplace_edit,
                email=email,
            )
            email_edit.save()
            i += 1
            go = f"email_{i}" in request.POST

        # Save the websites
        i = 1
        go = f"link_{i}" in request.POST
        while go:
            website = request.POST.get(f"link_{i}")
            website_edit = WebsiteEdit(
                marketplace=marketplace,
                marketplace_edit_id=marketplace_edit,
                website=website,
            )
            website_edit.save()
            i += 1
            go = f"link_{i}" in request.POST

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

    marketplace = Marketplace.objects.get(marketplace_url=marketplace_url)
    marketplace_edits = MarketplaceEdit.objects.filter(marketplace=marketplace)
    marketplace_edits_unreviewed = marketplace_edits.filter(is_reviewed=False)
    marketplace_edits_reviewed = marketplace_edits.filter(is_reviewed=True)
    phone_edits_unreviewed = PhoneEdit.objects.filter(marketplace=marketplace, is_reviewed=False)
    phone_edits_reviewed = PhoneEdit.objects.filter(marketplace=marketplace, is_reviewed=True)
    email_edits_unreviewed = EmailEdit.objects.filter(marketplace=marketplace, is_reviewed=False)
    email_edits_reviewed = EmailEdit.objects.filter(marketplace=marketplace, is_reviewed=True)
    website_edits_unreviewed = WebsiteEdit.objects.filter(marketplace=marketplace, is_reviewed=False)
    website_edits_reviewed = WebsiteEdit.objects.filter(marketplace=marketplace, is_reviewed=True)
    opening_hours_edits_unreviewed = OpeningHoursEdit.objects.filter(marketplace=marketplace, is_reviewed=False)
    opening_hours_edits_reviewed = OpeningHoursEdit.objects.filter(marketplace=marketplace, is_reviewed=True)

    features = ['fairground', 'indoor', 'toilets', 'handwashing', 'drinking_water', 'parking', 'bicycle_parking', 'food', 'drinks', 'handicrafts', 'butcher', 'dairy', 'seafood', 'garden_centre', 'florist']
    features_dict = {}
    for feature in features:
        features_dict[f"{feature}_yes"] = marketplace_edits.filter(**{feature: True}).count()
        features_dict[f"{feature}_no"] = marketplace_edits.filter(**{feature: False}).count()
        features_dict[f"{feature}_votes"] = features_dict[f"{feature}_yes"] + features_dict[f"{feature}_no"]

    context = {
        "marketplace": marketplace,
        "marketplace_edits_unreviewed": marketplace_edits_unreviewed,
        "marketplace_edits_reviewed": marketplace_edits_reviewed,
        "phone_edits_unreviewed": phone_edits_unreviewed,
        "phone_edits_reviewed": phone_edits_reviewed,
        "email_edits_unreviewed": email_edits_unreviewed,
        "email_edits_reviewed": email_edits_reviewed,
        "website_edits_unreviewed": website_edits_unreviewed,
        "website_edits_reviewed": website_edits_reviewed,
        "opening_hours_edits_unreviewed": opening_hours_edits_unreviewed,
        "opening_hours_edits_reviewed": opening_hours_edits_reviewed,
        "features_dict": features_dict,
    }
    
    return render(request, "revisiones_feria.html", context)


def revisiones_producto(request, product_url):
    return render(request, "revisiones_producto.html")
