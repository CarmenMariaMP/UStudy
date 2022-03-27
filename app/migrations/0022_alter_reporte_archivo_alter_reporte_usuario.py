# Generated by Django 4.0 on 2022-03-26 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_reporte_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='archivo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archivo', to='app.archivo'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='app.usuario'),
        ),
    ]
