# Generated by Django 4.0 on 2022-03-23 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_curso_asignatura_alter_curso_descripcion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='asignatura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.asignatura', verbose_name='Asignatura'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='descripcion',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='curso',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]