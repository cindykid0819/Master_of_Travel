from django.shortcuts import render
from .scrapers import Arrangement, Kkday, Eztravel, Klook

def index(request):
    arrangement = Arrangement(request.POST.get("sort_order"), request.POST.get("sort_condition"))

    klook = Klook(request.POST.get("city_name"), request.POST.get("lower_limit"), request.POST.get("upper_limit"))
    kkday = Kkday(request.POST.get("city_name"), request.POST.get("lower_limit"), request.POST.get("upper_limit"))
    eztravel = Eztravel(request.POST.get("city_name"), request.POST.get("lower_limit"), request.POST.get("upper_limit"))

    context = {
        "tickets": klook.scrape() + kkday.scrape() + eztravel.scrape(), "sortKey": arrangement.sortCondition(), "order": arrangement.sortOrder()
    }

    return render(request, "tickets/index.html", context)
