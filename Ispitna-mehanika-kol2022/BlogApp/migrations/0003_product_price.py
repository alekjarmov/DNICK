# Generated by Django 4.2.2 on 2023-06-05 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BlogApp", "0002_product_stock"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="price",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
