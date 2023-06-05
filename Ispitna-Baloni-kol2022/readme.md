The commands to initialize the project and the app are: (careful app and project names should be different) and keep the `.` in mind
```bash
pip install django Pillow # can try django-types and djnago-stubs as well for typing support
django-admin startproject <project_name> . # use a different project and app name
python manage.py startapp <app_name>
```

After that, add the "app_name" to the `INSTALLED_APPS` list in `settings.py`.

```bash
python manage.py makemigrations && python manage.py migrate # have to type these separately on PowerShell
python manage.py createsuperuser
python manage.py runserver
```

In the `settings.py` file of the project, add the following lines (so images can load):

```python
import os
MEDIA_ROOT = os.path.join(BASE_DIR, "data/")
MEDIA_URL = '/data/'
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
    path('index/', index, name='index'), # could be changed
    path('flights/', flights, name='flights') # could be changed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

A new file called `forms.py` should be added in the app. This will usually contain just 1 form, in this case for flight.

```python
from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FlightForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Flight
        exclude = ("user", )
```

Forms in the backend:

```python
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

#### Templating language tutorial
The base template can look something like this
```jinja
{%  include "navbar.html" %}

<div class="container main-container">

    {% block content %} {% endblock %}
</div>
```
The other templates can then extend it and look like this, if we dont want to extend a base template the include part is the most useful for the navbar or for a footer.
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
<strong>Important</strong> note always add `{% csrf_token %}` and the attribute `enctype="multipart/form-data"`in the forms.
Example form:
```jinja
    <form action="/flights/" method="POST" class="mb-4 px-3" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
```

Different CSS Properties
For div with a background image
```html
<div style="background-image: url('https://www.x.com'); width: 100%; background-position: center; background-size: cover; height: 500px;">
```

Bootstrap properties
```bash
d-flex # for flex
flex-column # for column flex
justify-content-between # for main flex axis (default x) to make the content at the begging and at the end used for navbars
align-items-center # secondary axis centering
justify-content-center primary axis centering
mb, mt, ms, me, mx, my same for padding b=bottom t=top, s=start, e=end 
<button class="btn btn-success rounded-pill"> for a button which is rounded
text-muted # for greyish text
```

Simplest bootstrap card
```html
        <div class="col-4">
            <div class="card" style="">
                <div style="height: 6rem;background: #5ec2a2" class="text-white text-center pt-3">
                    <span class="pt-5">Single</span>
                    <h3>$150</h3>
                </div>
                <div class="card-body text-center d-flex justify-content-center align-items-center flex-column py-4">
                    Some text is here
                </div>
                <div class="card-footer">
                    Card footer
                </div>
            </div>
        </div>
```


