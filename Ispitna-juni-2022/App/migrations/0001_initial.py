# Generated by Django 4.2.2 on 2023-06-06 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=50)),
                ("max_speed", models.PositiveIntegerField()),
                ("color", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Producer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("country_of_origin", models.CharField(max_length=50)),
                ("url", models.URLField()),
                ("owner_name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="WorkShop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("year_founded", models.PositiveIntegerField()),
                ("repairs_oldtimers", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Repair",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=50)),
                ("date", models.DateField()),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="images")),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="App.car"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "workshop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="App.workshop"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProducerWorkshop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "producer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="App.producer"
                    ),
                ),
                (
                    "workshop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="App.workshop"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="car",
            name="producer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="App.producer"
            ),
        ),
    ]
