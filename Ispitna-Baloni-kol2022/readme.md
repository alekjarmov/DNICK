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

