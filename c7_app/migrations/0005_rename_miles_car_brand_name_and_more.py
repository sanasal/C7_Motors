# Generated by Django 4.2.5 on 2024-12-22 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('c7_app', '0004_carscart_remove_customers_data_drop_off_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='miles',
            new_name='brand_name',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='name',
            new_name='exterior_color',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='gear',
            new_name='transmission',
        ),
        migrations.RemoveField(
            model_name='car',
            name='img',
        ),
        migrations.RemoveField(
            model_name='car',
            name='insurance',
        ),
        migrations.RemoveField(
            model_name='car',
            name='price',
        ),
        migrations.RemoveField(
            model_name='car',
            name='seats',
        ),
        migrations.RemoveField(
            model_name='car',
            name='year',
        ),
        migrations.AddField(
            model_name='car',
            name='cash_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='interior_color',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='car',
            name='mileage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='car',
            name='model_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='monthly_installments_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='CarImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='C7_Motors\\media')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='c7_app.car')),
            ],
        ),
    ]
