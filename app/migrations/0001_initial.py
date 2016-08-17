# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-17 16:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BasketballTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['school'],
            },
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_type', models.CharField(choices=[('Basketball', 'Basketball'), ('Football', 'Football')], default='Football', max_length=30)),
                ('checkin_body', models.TextField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Debate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debate_body', models.TextField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='FootballTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['school'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(blank=True, max_length=50, null=True)),
                ('location_city', models.CharField(blank=True, max_length=50, null=True)),
                ('location_address', models.CharField(blank=True, max_length=50, null=True)),
                ('location_zip', models.CharField(blank=True, max_length=10, null=True)),
                ('geolocation', geoposition.fields.GeopositionField(blank=True, max_length=42, null=True)),
            ],
            options={
                'ordering': ['location_name'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=10, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_photos', verbose_name='Profile Photo')),
                ('basketball', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.BasketballTeam')),
                ('football', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.FootballTeam')),
                ('prof_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.State'),
        ),
        migrations.AddField(
            model_name='debate',
            name='debate_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Location'),
        ),
        migrations.AddField(
            model_name='debate',
            name='debate_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='checkin',
            name='checkin_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Location'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='checkin_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
