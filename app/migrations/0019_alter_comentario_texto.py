# Generated by Django 3.2.7 on 2022-05-18 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_retiradadinero_fecha_alter_retiradadinero_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='texto',
            field=models.CharField(max_length=600),
        ),
    ]
