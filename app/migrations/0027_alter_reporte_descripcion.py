# Generated by Django 4.0.3 on 2022-03-28 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_archivo_fecha_publicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='descripcion',
            field=models.TextField(max_length=500),
        ),
    ]
