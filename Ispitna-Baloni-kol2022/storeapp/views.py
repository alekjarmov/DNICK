from django.shortcuts import render
from .forms import FlightForm
# Create your views here.


def index(request):
    return render(request, "index.html")


def flights(request):
    context = {}
    context['form'] = FlightForm()
    return render(request, 'flights.html', context=context)
