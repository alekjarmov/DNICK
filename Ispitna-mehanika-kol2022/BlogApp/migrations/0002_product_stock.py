# Generated by Django 4.2.2 on 2023-06-05 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BlogApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
