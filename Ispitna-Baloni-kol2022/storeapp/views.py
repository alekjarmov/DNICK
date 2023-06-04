from django.http import HttpRequest
from django.shortcuts import render, redirect
from .forms import FlightForm
from. models import Flight
# Create your views here.


def index(request):
    return render(request, "index.html")


def flights(request: HttpRequest):
    # check if anonymous user
    if not request.user.is_authenticated:
        return redirect("/admin/")

    context = dict()
    context["form"] = FlightForm

    if request.method == "POST":
        form_data = FlightForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            flight: Flight = form_data.save(commit=False)
            flight.user = request.user
            flight.picture = form_data.cleaned_data["picture"]
            flight.save()
            return redirect("flights")
    context["flights"] = Flight.objects.all()
    return render(request, "flights.html", context=context)
