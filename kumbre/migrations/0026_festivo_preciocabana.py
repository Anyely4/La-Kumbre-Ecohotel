# Generated by Django 5.1.4 on 2025-04-24 20:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kumbre', '0025_alter_reserva_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Festivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(unique=True)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PrecioCabana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_entre_semana', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_fin_semana', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_festivo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cabana', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='precios', to='kumbre.cabana')),
            ],
        ),
    ]
