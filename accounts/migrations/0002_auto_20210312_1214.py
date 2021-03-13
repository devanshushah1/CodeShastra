# Generated by Django 3.1.7 on 2021-03-12 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_type1',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_type2',
        ),
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(blank=True, default='India', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
