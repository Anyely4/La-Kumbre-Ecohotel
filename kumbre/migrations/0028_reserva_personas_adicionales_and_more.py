# Generated by Django 5.1.4 on 2025-04-25 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kumbre', '0027_preciocabana_precio_persona_adicional_entre_semana_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='personas_adicionales',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reserva',
            name='precio_personas_adicionales',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
