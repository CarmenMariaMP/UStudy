# Generated by Django 3.2.7 on 2022-04-27 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_merge_20220426_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archivos', to='app.curso', verbose_name='Curso'),
        ),
    ]
