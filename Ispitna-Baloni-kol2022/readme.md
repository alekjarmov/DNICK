
```bash
pip install django Pillow # maybe django-stubs djnago-types
django-admin startproject <project_name> . # notice the .
python manage.py startapp <app_name> # use a different project and app name
```

After that, add the "app_name" to the `INSTALLED_APPS` list in `settings.py`.

```bash
python manage.py makemigrations && python manage.py migrate # run separate
python manage.py createsuperuser
python manage.py runserver
```

In the `settings.py` file of the project, add the following lines (so images can load):

```python
import os
MEDIA_ROOT = os.path.join(BASE_DIR, "data/")
MEDIA_URL = '/data/'
```
Models possible fields with their required arguments
```py
class MyModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=False, Blank=False, default="LOL")
    category = models.ForeignKey(OtherModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    email = models.EmailField()
    stuff = models.ManyToManyField(OtherModel)
    
    def __str__(self):
        return f"{self.name}"
```
In `urls.py`, add the needed paths, in this case `/index/` and `/flights/`, as well as the static folder which should be the same regardless of the task. `views.py` should look like this:

```python
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from storeapp.views import index, flights # could be changed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'), # could be changed MUST HAVE name='something'
    path('flights/', flights, name='flights') # could be changed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

A new file called `forms.py` should be added in the app. This will usually contain just 1 form, in this case for flight.

```python
from django import forms
from .models import MyClass

class MyClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyClassForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = MyClass
        exclude = ("user", )
```

views.py in the backend:

```python
def flights(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/admin/")
    context = dict()
    if request.method == "POST":
        form_data = FlightForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            flight: Flight = form_data.save(commit=False)
            flight.user = request.user
            flight.image = form_data.cleaned_data["image"]
            flight.save()
            return redirect("flights")
    context["form"] = FlightForm
    context["flights"] = Flight.objects.filter(airport_takeoff=2, pilot__name="John").all()
    return render(request, "flights.html", context=context)
```

Useful imports:

```python
from django.contrib.auth.models import User
from django import forms
from .forms import MyForm
from typing import Optional
from django.http import HttpRequest
```

Admin panel stuff:

```python
class PublicationAuthorAdmin(admin.StackedInline): # for inline model, can use TabularInline too
    model = PublicationAuthor
    extra = 1 # always set to 1

class PublicationAdmin(admin.ModelAdmin):
    inlines = [PublicationAuthorAdmin] # to register the inline models

    list_display = ("first_name", "last_name")
    exclude = ('company', )
    readonly_fields = ('user', )
    list_filter = ['user']
    search_fields = ['user']

    def has_change_permission(self, request, obj=None):
        pass
    def has_delete_permission(self, request, obj=None):
        pass
    def has_delete_permission(self, request, obj=None):
        pass
    def has_view_permission(self, request, obj=None):
        pass
    def save_model(self, request: HttpRequest, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
    def get_queryset(self, request): # wrong model to show example
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        blocked = BlockList.objects.filter(user__user=request.user).values_list(
            "user", flat=True
        )
        return qs.exclude(author__user__in=blocked)

admin.site.register(Publication, PublicationAdmin)
```
### Frontend
In the app module create a folder called `templates` where the templates will be stored.

The base template can look something like this:
```jinja
{%  include "navbar.html" %}
<div class="container main-container">
    {% block content %} {% endblock %}
</div>
```
The other templates can then extend it or just `{%  include "navbar.html" %}`
```jinja
{% extends 'base.html' %}
{% block content %}
    <ul>
    {% for user in blocked %}
        <li>{{ user }}</li>
    {% endfor %}
    </ul>
{% endblock %}
```
Form in frontend:
```jinja
    <form action="/flights/" method="POST" class="mb-4 px-3" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
```

Different CSS Properties
For div with a background image and for a bold underline
```html
<div style="background-image: url('https://www.x.com'); width: 100%; background-position: center; background-size: cover; height: 500px;">
<div class="d-flex justify-content-center">
  <div class="border-bottom border-3 border-success align-self-center " style="width:8rem"></div>
</div>
```

Bootstrap properties
```bash
d-flex # for flex
flex-column # for column flex
justify-content-between # for main flex axis (default x) to make the content at the begging and at the end used for navbars
align-items-center # secondary axis centering
justify-content-center primary axis centering
gap-x, g-x, gb-2, gap-2 # to change space between columns/rows g and flex elements gap
mb, mt, ms, me, mx, my same for padding b=bottom t=top, s=start, e=end 
<button class="btn btn-success rounded-pill"> for a button which is rounded
text-muted # for greyish text
```
Simple card
```jinja
        <div class="card border-light col-3 my-3 border-0" style="">
            <img src="{{product.image.url}}" class="card-img-top" alt="...">
            <div class="card-body text-center">
                <p class="card-text text-center">
                <div class="text-muted">
                    {{product.name}}
                </div>
                <h6 class="font-weight-bold">${{product.price}}</h6>
                </p>
            </div>
        </div>
```
