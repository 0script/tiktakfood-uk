# Generated by Django 4.2.5 on 2023-09-12 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_categorymenu_restaurantmenu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantmenu',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
