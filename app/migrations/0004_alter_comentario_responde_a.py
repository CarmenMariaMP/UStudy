# Generated by Django 3.2.7 on 2022-04-15 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_comentario_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='responde_a',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.comentario', verbose_name='Responde a'),
        ),
    ]
