# Generated by Django 4.0 on 2022-03-16 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_notificacion_comentario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='id_refencia',
            field=models.SmallIntegerField(null=True),
        ),
    ]
