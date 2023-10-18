from django.shortcuts import render, redirect
from marketplaces.models import Marketplace, MarketplaceHistory
from products.models import Product, Variety
from .models import (
    MarketplaceEdit,
    MarketplaceProductsEdit,
    OpeningHoursEdit,
    PhoneEdit,
    EmailEdit,
    WebsiteEdit,
)
import osm_opening_hours_humanized as hoh
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import ast
from datetime import datetime

# Create your views here.


def sugerencias(request):
    marketplaces = Marketplace.objects.all()
    products = Product.objects.all()
    context = {
        "marketplaces": marketplaces,
        "products": products,
    }
    return render(request, "sugerencias.html", context)


def sugerencias_gracias(request):
    return render(request, "sugerencias_gracias.html")


def sugerencias_ferias(request):
    marketplaces = Marketplace.objects.all()
    context = {
        "marketplaces": marketplaces,
    }
    return render(request, "sugerencias_ferias.html", context)


def sugerencias_productos(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "sugerencias_productos.html", context)


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
        marketplace_edit.drinking_water = ast.literal_eval(
            request.POST.get("drinking_water")
        )
        marketplace_edit.parking = ast.literal_eval(request.POST.get("parking"))
        marketplace_edit.bicycle_parking = ast.literal_eval(
            request.POST.get("bicycle_parking")
        )

        # Services
        marketplace_edit.food = ast.literal_eval(request.POST.get("food"))
        marketplace_edit.drinks = ast.literal_eval(request.POST.get("drinks"))
        marketplace_edit.handicrafts = ast.literal_eval(request.POST.get("handicrafts"))
        marketplace_edit.butcher = ast.literal_eval(request.POST.get("butcher"))
        marketplace_edit.dairy = ast.literal_eval(request.POST.get("dairy"))
        marketplace_edit.seafood = ast.literal_eval(request.POST.get("seafood"))
        marketplace_edit.garden_centre = ast.literal_eval(
            request.POST.get("garden_centre")
        )
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


def sugerencias_feria_productos(request, marketplace_url):
    marketplace = Marketplace.objects.get(marketplace_url=marketplace_url)

    if request.method == "POST":
        marketplace_products_edit = MarketplaceProductsEdit()
        marketplace_products_edit.marketplace = marketplace

        varieties = request.POST.dict()
        varieties.pop("csrfmiddlewaretoken")
        varieties.pop("submitted_by")

        marketplace_products_edit.varieties = varieties
        marketplace_products_edit.submitted_by = request.POST.get("submitted_by")
        marketplace_products_edit.save()

        print(f"\nPost:\n{request.POST}\n")

        context = {"marketplace": marketplace}
        return redirect("sugerencias_gracias")
    else:
        varieties = Variety.objects.all().order_by("product_url")
        varieties_otros = varieties.filter(product_url__category="otro")
        varieties_frutas = varieties.filter(product_url__category="fruta")
        varieties_hierbas = varieties.filter(product_url__category="hierba")
        varieties_verduras = varieties.filter(product_url__category="verdura")
        varieties_legumbres = varieties.filter(product_url__category="legumbre")
        varieties_tuberculos = varieties.filter(product_url__category="tubérculo")
        context = {
            "marketplace": marketplace,
            "varieties_otros": varieties_otros,
            "varieties_frutas": varieties_frutas,
            "varieties_hierbas": varieties_hierbas,
            "varieties_verduras": varieties_verduras,
            "varieties_legumbres": varieties_legumbres,
            "varieties_tuberculos": varieties_tuberculos,
        }
        return render(request, "sugerencias_feria_productos.html", context)


def sugerencias_producto(request, product_url):
    product = Product.objects.get(product_url=product_url)
    context = {"product": product}
    return render(request, "sugerencias_producto.html", context)


def revisiones(request):
    marketplaces = Marketplace.objects.all()
    products = Product.objects.all()
    context = {
        "marketplaces": marketplaces,
        "products": products,
    }
    return render(request, "revisiones.html", context)


def revisiones_ferias(request):
    return render(request, "revisiones_ferias.html")


def revisiones_productos(request):
    return render(request, "revisiones_productos.html")


@login_required(login_url="/ingresar/")
def revisiones_feria(request, marketplace_url):
    marketplace = Marketplace.objects.get(marketplace_url=marketplace_url)
    marketplace_edits = MarketplaceEdit.objects.filter(marketplace=marketplace)
    marketplace_edits_unreviewed = marketplace_edits.filter(is_reviewed=False)
    marketplace_edits_reviewed = marketplace_edits.filter(is_reviewed=True)
    phone_edits_unreviewed = PhoneEdit.objects.filter(
        marketplace=marketplace, is_reviewed=False
    )
    email_edits_unreviewed = EmailEdit.objects.filter(
        marketplace=marketplace, is_reviewed=False
    )
    website_edits_unreviewed = WebsiteEdit.objects.filter(
        marketplace=marketplace, is_reviewed=False
    )
    opening_hours_edits_unreviewed = OpeningHoursEdit.objects.filter(
        marketplace=marketplace, is_reviewed=False
    )

    if request.method == "POST":
        # Save outdated version of marketplace in history
        marketplace_history = MarketplaceHistory()
        marketplace_history.marketplace_history_id = (
            f"{marketplace.marketplace_url}_{datetime.now()}"
        )
        marketplace_history.marketplace = marketplace
        marketplace_history.name = marketplace.name
        marketplace_history.name_alternate = marketplace.name_alternate
        marketplace_history.description = marketplace.description
        marketplace_history.opening_hours = marketplace.opening_hours
        marketplace_history.opening_date = marketplace.opening_date
        marketplace_history.location = marketplace.location
        marketplace_history.area = marketplace.area
        marketplace_history.province = marketplace.province
        marketplace_history.canton = marketplace.canton
        marketplace_history.district = marketplace.district
        marketplace_history.postal_code = marketplace.postal_code
        marketplace_history.address = marketplace.address
        marketplace_history.size = marketplace.size
        marketplace_history.phone = marketplace.phone
        marketplace_history.email = marketplace.email
        marketplace_history.website = marketplace.website
        marketplace_history.instagram = marketplace.instagram
        marketplace_history.facebook = marketplace.facebook
        marketplace_history.operator = marketplace.operator
        marketplace_history.branch = marketplace.branch
        marketplace_history.parking = marketplace.parking
        marketplace_history.bicycle_parking = marketplace.bicycle_parking
        marketplace_history.fairground = marketplace.fairground
        marketplace_history.indoor = marketplace.indoor
        marketplace_history.toilets = marketplace.toilets
        marketplace_history.handwashing = marketplace.handwashing
        marketplace_history.drinking_water = marketplace.drinking_water
        marketplace_history.food = marketplace.food
        marketplace_history.drinks = marketplace.drinks
        marketplace_history.handicrafts = marketplace.handicrafts
        marketplace_history.butcher = marketplace.butcher
        marketplace_history.dairy = marketplace.dairy
        marketplace_history.seafood = marketplace.seafood
        marketplace_history.garden_centre = marketplace.garden_centre
        marketplace_history.florist = marketplace.florist
        marketplace_history.other_services = marketplace.other_services
        marketplace_history.updated_by = request.user
        marketplace_history.comments_reviewer = request.POST.get("comments_reviewer")
        marketplace_history.save()

        marketplace_history.payment.set(marketplace.payment.all())
        marketplace_history.products.set(marketplace.products.all())
        marketplace_history.save()

        # Update marketplace with new information
        name = request.POST.get("name")
        if (name != "") and (name != marketplace.name):
            marketplace.name = name
        name_alternate = request.POST.get("name_alternate")
        if (name_alternate != "") and (name_alternate != marketplace.name_alternate):
            marketplace.name_alternate = name_alternate
        operator = request.POST.get("operator")
        if (operator != "") and (operator != marketplace.operator):
            marketplace.operator = operator
        phone = request.POST.get("phone")
        if (phone != "") and (phone != marketplace.phone):
            marketplace.phone = phone
        email = request.POST.get("email")
        if (email != "") and (email != marketplace.email):
            marketplace.email = email
        website = request.POST.get("website")
        if (website != "") and (website != marketplace.website):
            marketplace.website = website
        description = request.POST.get("description")
        if (description != "") and (description != marketplace.description):
            marketplace.description = description
        address = request.POST.get("address")
        if (address != "") and (address != marketplace.address):
            marketplace.address = address
        size = request.POST.get("size")
        if size != marketplace.size:
            marketplace.size = size
        opening_hours = request.POST.get("opening_hours")
        if (opening_hours != "") and (opening_hours != marketplace.opening_hours):
            marketplace.opening_hours = opening_hours
        opening_date = request.POST.get("opening_date")
        if (opening_date != "") and (opening_date != marketplace.opening_date):
            marketplace.opening_date = opening_date
        fairground = ast.literal_eval(request.POST.get("fairground"))
        if fairground != marketplace.fairground:
            marketplace.fairground = fairground
        indoor = ast.literal_eval(request.POST.get("indoor"))
        if indoor != marketplace.indoor:
            marketplace.indoor = indoor
        toilets = ast.literal_eval(request.POST.get("toilets"))
        if toilets != marketplace.toilets:
            marketplace.toilets = toilets
        handwashing = ast.literal_eval(request.POST.get("handwashing"))
        if handwashing != marketplace.handwashing:
            marketplace.handwashing = handwashing
        drinking_water = ast.literal_eval(request.POST.get("drinking_water"))
        if drinking_water != marketplace.drinking_water:
            marketplace.drinking_water = drinking_water
        parking = request.POST.get("parking")
        if (parking != "") and (parking != marketplace.parking):
            marketplace.parking = parking
        bicycle_parking = ast.literal_eval(request.POST.get("bicycle_parking"))
        if bicycle_parking != marketplace.bicycle_parking:
            marketplace.bicycle_parking = bicycle_parking
        food = ast.literal_eval(request.POST.get("food"))
        if food != marketplace.food:
            marketplace.food = food
        drinks = ast.literal_eval(request.POST.get("drinks"))
        if drinks != marketplace.drinks:
            marketplace.drinks = drinks
        handicrafts = ast.literal_eval(request.POST.get("handicrafts"))
        if handicrafts != marketplace.handicrafts:
            marketplace.handicrafts = handicrafts
        butcher = ast.literal_eval(request.POST.get("butcher"))
        if butcher != marketplace.butcher:
            marketplace.butcher = butcher
        dairy = ast.literal_eval(request.POST.get("dairy"))
        if dairy != marketplace.dairy:
            marketplace.dairy = dairy
        seafood = ast.literal_eval(request.POST.get("seafood"))
        if seafood != marketplace.seafood:
            marketplace.seafood = seafood
        garden_centre = ast.literal_eval(request.POST.get("garden_centre"))
        if garden_centre != marketplace.garden_centre:
            marketplace.garden_centre = garden_centre
        florist = ast.literal_eval(request.POST.get("florist"))
        if florist != marketplace.florist:
            marketplace.florist = florist

        marketplace.save()

        # Update the marketplace edit objects as reviewed
        marketplace_edits_unreviewed.update(is_reviewed=True, reviewed_by=request.user)

        # Update phones, emails and websites as reviewed if checkbox is on
        if request.POST.get("check-phone"):
            phone_edits_unreviewed.update(is_reviewed=True, reviewed_by=request.user)
        if request.POST.get("check-email"):
            email_edits_unreviewed.update(is_reviewed=True, reviewed_by=request.user)
        if request.POST.get("check-website"):
            website_edits_unreviewed.update(is_reviewed=True, reviewed_by=request.user)

        # Redirect to the marketplace page
        return redirect(f"/ferias/{marketplace_url}/")

    else:
        if request.user.is_staff:
            phone_edits_reviewed = PhoneEdit.objects.filter(
                marketplace=marketplace, is_reviewed=True
            )
            email_edits_reviewed = EmailEdit.objects.filter(
                marketplace=marketplace, is_reviewed=True
            )
            website_edits_reviewed = WebsiteEdit.objects.filter(
                marketplace=marketplace, is_reviewed=True
            )
            opening_hours_edits_reviewed = OpeningHoursEdit.objects.filter(
                marketplace=marketplace, is_reviewed=True
            )

            features = [
                "fairground",
                "indoor",
                "toilets",
                "handwashing",
                "drinking_water",
                "parking",
                "bicycle_parking",
                "food",
                "drinks",
                "handicrafts",
                "butcher",
                "dairy",
                "seafood",
                "garden_centre",
                "florist",
            ]
            features_dict = {}
            for feature in features:
                features_dict[f"{feature}_yes"] = marketplace_edits.filter(
                    **{feature: True}
                ).count()
                features_dict[f"{feature}_no"] = marketplace_edits.filter(
                    **{feature: False}
                ).count()
                features_dict[f"{feature}_votes"] = (
                    features_dict[f"{feature}_yes"] + features_dict[f"{feature}_no"]
                )

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
        else:
            return redirect("/")


def revisiones_producto(request, product_url):
    return render(request, "revisiones_producto.html")
