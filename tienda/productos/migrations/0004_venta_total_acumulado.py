# Generated by Django 4.2.11 on 2024-04-15 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_venta'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='total_acumulado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]