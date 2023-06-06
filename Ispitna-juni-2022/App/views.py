from django.http import HttpRequest
from django.shortcuts import render, redirect

from App.forms import RepairForm
from App.models import Repair


# Create your views here.
def index(request):
    return render(request, 'index.html')


def repairs(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/admin/")

    if request.method == "POST":
        form_data = RepairForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            repair: Repair = form_data.save(commit=False)
            repair.user = request.user
            repair.image = form_data.cleaned_data['image']
            repair.save()
            redirect("repairs")

    context = dict()
    context["form"] = RepairForm()
    context["repairs"] = Repair.objects.filter(user=request.user, car__type='Sedan').all()
    return render(request, 'repairs.html', context=context)
