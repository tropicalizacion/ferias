from django.shortcuts import render
from marketplaces.models import Marketplace
from .models import MarketplaceEdit, PhotoEdit

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
            # location=request.POST["location"],
            # area=request.POST["area"],
            # province=request.POST["province"],
            # canton=request.POST["canton"],
            # district=request.POST["district"],
            # postal_code=request.POST["postal_code"],
            # address=request.POST["address"],
            # size=request.POST["size"],
            # phone=request.POST["phone"],
            # email=request.POST["email"],
            # website=request.POST["website"],
            # operator=request.POST["operator"],
            # branch=request.POST["branch"],
            # parking=request.POST["parking"],
            # bicycle_parking=request.POST["bicycle_parking"],
            # fairground=request.POST["fairground"],
            # indoor=request.POST["indoor"],
        )
        marketplace_edit.save()
        # for photo in request.FILES.getlist("photos"):
        #     photo_edit = PhotoEdit.objects.create(
        #         marketplace_edit=marketplace_edit, photo=photo
        #     )
        #     photo_edit.save()
        return render(request, "sugerencia.html", {"marketplace": marketplace})
    else:
        marketplace = Marketplace.objects.get(marketplace_url=marketplace_url)
        context = {"marketplace": marketplace}
        return render(request, "sugerencia.html", context)


def revisiones(request):
    return render(request, "revisiones.html")


def revision(request, marketplace_url):
    return render(request, "revision.html")
