# Generated by Django 4.2.5 on 2023-09-14 12:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0010_alter_itemquantity_whishlist_order_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='OrderRestaurant',
        ),
    ]
