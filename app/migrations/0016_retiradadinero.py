# Generated by Django 4.0 on 2022-04-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_ticketdescarga_archivo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetiradaDinero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('dinero', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
    ]
