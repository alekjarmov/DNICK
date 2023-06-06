from django.http import HttpRequest
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product


# Create your views here.
def index(request: HttpRequest):
    return render(request, 'index.html')


def outofstock(request: HttpRequest):
    context = dict()
    if not request.user.is_authenticated:
        return redirect('/admin/')

    if request.method == "POST":
        form_data = ProductForm(data = request.POST, files=request.FILES)
        if form_data.is_valid():
            product: Product = form_data.save(commit=False)
            product.user = request.user
            product.image = form_data.cleaned_data["image"]
            product.save()
            return redirect("outofstock")

    products = Product.objects.filter(stock=0, category__is_active=True).all()
    context["products"] = products
    context["form"] = ProductForm
    return render(request, "outofstock.html", context=context)