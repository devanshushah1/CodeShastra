# Generated by Django 3.1.7 on 2021-03-13 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_claims_bill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='is_found',
        ),
    ]
