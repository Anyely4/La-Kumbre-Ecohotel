# Generated by Django 5.1.6 on 2025-02-28 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kumbre', '0016_rename_nombre_sugerencia_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabana',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='cabana',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
