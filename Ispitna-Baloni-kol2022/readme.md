```bash
pip install django django-types Pillow # substitute django-stubs for django-stubs maybe
```
The commands to initialize the project and the app are: (careful app and project names should be different) and keep the `.` in mind
```bash
django-admin startproject <project_name> . # use a different project and app name
python manage.py startapp <app_name>
```

After that, add the app to the `INSTALLED_APPS` list in `settings.py`.

```bash
python manage.py makemigrations && python manage.py migrate # have to type these separately on PoweShell
```

```bash
python manage.py createsuperuser
```

```bash
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
def add(request):
    if request.method == "POST":
        form_data = BookForm(data=request.POST, files=request.FILES) # always the same, just change the Form class
        if form_data.is_valid():
            book = form_data.save(commit=False) # make commit=false so new changes can be made
            book.user = request.user
            book.cover_image = form_data.cleaned_data['cover_image'] # ImageFields should be handled like this
            book.save()
            return redirect("list") # name of where we want to redirect

    return render(request, "add.html", context={"form": BookForm})
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
Different CSS Properties
For background image
```html
<div style="background-image: url('https://www.x.com'); width: 100%; background-position: center; background-size: cover; height: 500px;">
```
