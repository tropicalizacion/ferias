from django.shortcuts import render
from marketplaces.models import Marketplace
from .models import MarketplaceEdit, PhotoEdit, OpeningHoursEdit

# Create your views here.


def sugerencias(request):
    marketplaces = Marketplace.objects.all()
    context = {"marketplaces": marketplaces}
    return render(request, "sugerencias.html", context)


def sugerencia(request, marketplace_url):
    if request.method == "POST":
        marketplace = Marketplace.objects.get(marketplace_url=marketplace_url)
        marketplace_edit = MarketplaceEdit(
            marketplace=marketplace,
            name=request.POST.get("name"),
            name_alternate=request.POST.get("name_alternate"),
            description=request.POST.get("description"),
            # opening_hours=request.POST["opening_hours"],
            # opening_date=request.POST["opening_date"],
            location=request.POST.get("location"),
            address=request.POST.get("address"),
            size=request.POST.get("size"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            website=request.POST.get("website"),
        )
        marketplace_edit.save()
        openingHours_edit = OpeningHoursEdit(
            marketplace=marketplace,
            day_opens = request.POST.get("day_opens"),
            hour_opens = request.POST.get("hour_opens"),
            day_closes = request.POST.get("day_closes"),
            hour_closes = request.POST.get("hour_closes"),
	)
        openingHours_edit.save()
        return render(request, "sugerencia.html",{"marketplace": marketplace})
    else:
        marketplace = Marketplace.objects.get(marketplace_url=marketplace_url)
        size_choices = marketplace.SIZE_CHOICES
        openingHours_edit = OpeningHoursEdit()
        day_choices = openingHours_edit.DAY_CHOICES
        hour_choices = openingHours_edit.HOUR_CHOICES
        context = {
          "marketplace": marketplace,
          "size_choices": size_choices,
          "day_choices": day_choices,
          "hour_choices": hour_choices,
        }
        return render(request, "sugerencia.html", context)


def revisiones(request):
    return render(request, "revisiones.html")


def revision(request, marketplace_url):
    return render(request, "revision.html")
