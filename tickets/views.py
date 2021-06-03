from django.shortcuts import render
#from .scrapers import Klook, Kkday
from .scrapers import Kkday, Eztravel

def index(request):

    #klook = Klook(request.POST.get("city_name"))
    #kkday = Kkday(request.POST.get("city_name"))
    eztravel = Eztravel(request.POST.get("city_name"))

    context = {
        #"tickets": kkday.scrape()
        #"tickets": klook.scrape() + kkday.scrape()
        "tickets": eztravel.scrape()
    }

    return render(request, "tickets/index.html", context)
