# Generated by Django 4.2.5 on 2023-09-13 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_restaurantmenu_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantmenu',
            name='image',
            field=models.ImageField(upload_to='restaurant_images/'),
        ),
    ]
