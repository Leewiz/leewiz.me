# Generated by Django 5.1.2 on 2024-11-25 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gtfs_rt', '0005_alter_subwayentity_start_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subwaystoptimeupdate',
            unique_together={('arrival_time', 'departure_time', 'stop_id')},
        ),
    ]
