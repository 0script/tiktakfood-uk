# Generated by Django 4.2.5 on 2023-09-08 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_menuitem_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordermodel',
            old_name='state',
            new_name='province',
        ),
    ]
