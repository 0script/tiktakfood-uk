# Generated by Django 4.2.5 on 2023-09-17 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_alter_restaurantmenu_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderrestaurant',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
    ]
