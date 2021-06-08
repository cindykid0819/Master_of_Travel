from django.shortcuts import render
from .scrapers import Arrangement, Kkday, Eztravel, Klook

def index(request):
    arrangement = Arrangement(request.POST.get("sort_order"), request.POST.get("sort_condition"))
    klook = Klook(request.POST.get("city_name"))
    #kkday = Kkday(request.POST.get("city_name"))
    eztravel = Eztravel(request.POST.get("city_name"))

    context = {
        "tickets": klook.scrape() + eztravel.scrape(), "sortKey": arrangement.sortCondition(), "order": arrangement.sortOrder()
    }

    return render(request, "tickets/index.html", context)
