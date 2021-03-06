# Generated by Django 3.2.6 on 2021-08-21 07:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_code', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False, unique=True, verbose_name='Event Code')),
                ('day', models.SmallIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], verbose_name='Day')),
                ('start', models.TimeField(max_length=5, verbose_name='Start Time')),
                ('end', models.TimeField(max_length=5, verbose_name='End Time')),
                ('title', models.CharField(max_length=256, verbose_name='Event Title')),
                ('description', models.TextField(verbose_name='Event Description')),
                ('image', models.ImageField(upload_to='uploads/', verbose_name='Event Banner')),
                ('seats', models.IntegerField(default=0, verbose_name='Event Seats')),
                ('max_seats', models.IntegerField(default=0, verbose_name='Maximum Event Seats')),
                ('category', models.CharField(choices=[('C', 'Cultural'), ('S', 'Sports')], max_length=1, verbose_name='Category')),
                ('is_seminar', models.BooleanField(default=False, verbose_name='Is Event a Seminar')),
                ('team_size', models.IntegerField(default=1, verbose_name='Team Size')),
                ('is_team_size_strict', models.BooleanField(verbose_name='Is Team Size Strict')),
                ('entry_fee', models.IntegerField(verbose_name='Entry Fee')),
                ('prize_money', models.TextField(verbose_name='Prize Money JSON')),
            ],
        ),
    ]
