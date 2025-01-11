# Generated by Django 4.2.5 on 2024-12-19 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c7_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='economy_reservation',
            name='car',
        ),
        migrations.RemoveField(
            model_name='economy_reservation',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='luxury_booking',
            name='lux_car',
        ),
        migrations.RemoveField(
            model_name='luxury_reservation',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='luxury_reservation',
            name='lux_car',
        ),
        migrations.RemoveField(
            model_name='premium_booking',
            name='pre_car',
        ),
        migrations.RemoveField(
            model_name='premium_reservation',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='premium_reservation',
            name='pre_car',
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='economy_car',
        ),
        migrations.DeleteModel(
            name='economy_reservation',
        ),
        migrations.DeleteModel(
            name='Luxury_Booking',
        ),
        migrations.DeleteModel(
            name='luxury_car',
        ),
        migrations.DeleteModel(
            name='luxury_reservation',
        ),
        migrations.DeleteModel(
            name='Premium_Booking',
        ),
        migrations.DeleteModel(
            name='premium_car',
        ),
        migrations.DeleteModel(
            name='premium_reservation',
        ),
    ]