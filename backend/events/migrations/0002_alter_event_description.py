# Generated by Django 3.2.6 on 2021-08-23 06:22

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=martor.models.MartorField(verbose_name='Event Description'),
        ),
    ]
