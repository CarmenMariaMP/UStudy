# Generated by Django 4.0 on 2022-03-26 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_reporte_archivo_reporte_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
    ]