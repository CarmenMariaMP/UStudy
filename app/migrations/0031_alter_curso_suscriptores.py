# Generated by Django 4.0 on 2022-03-30 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_merge_20220330_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='suscriptores',
            field=models.ManyToManyField(blank=True, related_name='Suscriptores', to='app.Usuario'),
        ),
    ]