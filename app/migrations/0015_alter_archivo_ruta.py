# Generated by Django 4.0 on 2022-03-19 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_archivo_fecha_publicacion_alter_archivo_ruta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='ruta',
            field=models.FileField(upload_to=''),
        ),
    ]
