# Generated by Django 4.0.3 on 2022-05-17 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_resenya_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resenya',
            name='descripcion',
            field=models.TextField(max_length=500),
        ),
    ]
