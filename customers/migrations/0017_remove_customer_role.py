# Generated by Django 5.1.3 on 2024-12-15 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0016_address_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='role',
        ),
    ]