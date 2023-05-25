The commands to initialize the project and the app are: (careful app and project names should be different)
```bash
django-admin startproject BalloonStore .
python manage.py startapp storeapp
```
After that you should add the app to the INSTALLED_APPS list in the settings.py file.

To make migrations and migrate the database:
```bash
python manage.py makemigrations && python manage.py migrate
```
To create a superuser:
```bash
python manage.py createsuperuser
```
To run the server:
```bash
python manage.py runserver
```

In the settings.py file of the project you should add the following lines(so images can load):
```python
import os
MEDIA_ROOT = os.path.join(BASE_DIR, "data/")
MEDIA_URL = '/data/'
```

In the urls.py of the PROJECT add the needed paths in this case /index/ and /flights/
as well as the static folder which should be the same regardless of the task. The views.py file should
look like this:
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
A new file called forms.py should be added in the app.
This will usually contain just 1 form in this case for flight.
```python
from django import forms
from .models import Flight


class FlightForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FlightForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            print(field)
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Flight
        exclude = ("user", )
```