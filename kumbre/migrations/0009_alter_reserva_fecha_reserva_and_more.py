# Generated by Django 5.1.4 on 2025-02-10 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kumbre', '0008_cabaña_created_at_reserva_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='fecha_reserva',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='activation_token',
            field=models.CharField(default='a27e268ea9654b6bb51780be441a1232', max_length=64, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='reserva',
            unique_together={('cabaña', 'fecha_reserva')},
        ),
    ]
