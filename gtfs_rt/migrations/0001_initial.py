# Generated by Django 5.1.2 on 2024-11-18 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubwayStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=10)),
                ('stop_name', models.CharField(max_length=100)),
                ('complex_id', models.CharField(max_length=100)),
                ('division', models.CharField(max_length=100)),
                ('borough', models.CharField(max_length=100)),
                ('north_direction_label', models.CharField(max_length=100)),
                ('south_direction_label', models.CharField(max_length=100)),
                ('line', models.CharField(max_length=100)),
                ('daytime_routes', models.CharField(max_length=100)),
                ('structure', models.CharField(max_length=100)),
                ('gtfs_stop_id', models.CharField(max_length=100)),
                ('gtfs_latitude', models.CharField(max_length=100)),
                ('gtfs_longitude', models.CharField(max_length=100)),
                ('ada_notes', models.CharField(max_length=100, null=True)),
                ('ada', models.CharField(max_length=100)),
                ('ada_northbound', models.CharField(max_length=100)),
                ('ada_southbound', models.CharField(max_length=100)),
                ('cbd', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubwayEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_id', models.CharField(max_length=100)),
                ('trip_id', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('start_date', models.DateTimeField()),
                ('route_id', models.CharField(max_length=100)),
                ('travel_direction', models.CharField(max_length=100)),
            ],
        ),   
    ]