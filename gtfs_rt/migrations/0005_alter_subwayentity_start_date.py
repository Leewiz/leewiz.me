# Generated by Django 5.1.2 on 2024-11-25 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtfs_rt', '0004_alter_subwayentity_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subwayentity',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='subwayentity',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
