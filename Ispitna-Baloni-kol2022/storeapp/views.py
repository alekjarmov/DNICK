from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")


def flights(request):
    return render(request, 'flights.html')
