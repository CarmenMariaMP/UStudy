# Generated by Django 4.0 on 2022-04-20 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketDescarga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Archivo', to='app.usuario')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Usuario', to='app.usuario')),
            ],
        ),
    ]
