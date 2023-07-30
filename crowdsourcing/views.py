from django.shortcuts import render
from marketplaces.models import Marketplace
from .models import MarketplaceEdit, PhotoEdit, OpeningHoursEdit
import osm_opening_hours_humanized as hoh

# Create your views here.


def sugerencias(request):
    marketplaces = Marketplace.objects.all()
    context = {"marketplaces": marketplaces}
    return render(request, "sugerencias.html", context)


def sugerencia(request, marketplace_url):
    if request.method == "POST":
        marketplace = Marketplace.objects.get(marketplace_url=marketplace_url)
        print(request.POST)
        marketplace_edit = MarketplaceEdit(
            marketplace=marketplace,
            name=request.POST.get("name"),
            name_alternate=request.POST.get("name_alternate"),
            operator=request.POST.get("operator"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            website=request.POST.get("website"),
            description=request.POST.get("description"),
            address=request.POST.get("address"),
            size=request.POST.get("size"),
            # opening_hours=request.POST["opening_hours"],
            opening_date=request.POST["opening_date"],
            fairground=request.POST.get("fairground"),
            indoor=request.POST.get("indoor"),
            toilets=request.POST.get("toilets"),
            handwashing=request.POST.get("handwashing"),
            drinking_water=request.POST.get("drinking_water"),
            parking=request.POST.get("parking"),
            bycicle_parking=request.POST.get("bycicle_parking"),
            food=request.POST.get("food"),
            drinks=request.POST.get("drinks"),
            handicrats=request.POST.get("handicrats"),
            butcher=request.POST.get("butcher"),
            dairy=request.POST.get("dairy"),
            seafood=request.POST.get("seafood"),
            garden_centre=request.POST.get("garden_centre"),
            florist=request.POST.get("florist"),
            comments=request.POST.get("comments"),
        )
        marketplace_edit.save()
        opening_hours_edit = OpeningHoursEdit(
            marketplace=marketplace,
            day_opens=request.POST.get("day_opens"),
            hour_opens=request.POST.get("hour_opens"),
            day_closes=request.POST.get("day_closes"),
            hour_closes=request.POST.get("hour_closes"),
        )
        opening_hours_edit.save()
        context = {"marketplace": marketplace}
        return render(request, "sugerencia.html", context)
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
        return render(request, "sugerencia.html", context)


def revisiones(request):
    return render(request, "revisiones.html")


def revision(request, marketplace_url):
    return render(request, "revision.html")
