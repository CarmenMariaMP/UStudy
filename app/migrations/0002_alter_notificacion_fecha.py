# Generated by Django 4.0 on 2022-04-12 15:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='fecha',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]