# Generated by Django 4.0.3 on 2022-04-06 08:30

import app.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('fecha_publicacion', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('ruta', models.FileField(upload_to=app.models.user_directory_path, validators=[app.models.validador_archivo])),
            ],
        ),
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('titulacion', models.CharField(max_length=200)),
                ('anyo', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('fecha_publicacion', models.DateField()),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.asignatura', verbose_name='Asignatura')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('nombre', models.CharField(max_length=40)),
                ('apellidos', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('email_academico', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True, validators=[app.models.validador_email])),
                ('titulacion', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True, max_length=500)),
                ('foto', models.ImageField(blank=True, null=True, upload_to=app.models.image_directory_path)),
                ('dinero', models.DecimalField(decimal_places=2, max_digits=12)),
                ('django_user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.curso', verbose_name='Curso')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuario', verbose_name='Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(max_length=500)),
                ('fecha', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('tipo', models.CharField(choices=[('PLAGIO', 'Plagio'), ('ERROR', 'Error')], max_length=10)),
                ('archivo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archivo', to='app.archivo')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='app.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_refencia', models.SmallIntegerField(null=True)),
                ('tipo', models.CharField(choices=[('COMENTARIO', 'Comentario'), ('REPORTE', 'Reporte'), ('NUEVO_ALUMNO', 'Nuevo Alumno')], max_length=20)),
                ('fecha', models.DateField()),
                ('visto', models.BooleanField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuario', verbose_name='Usuario')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='propietario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Propietario', to='app.usuario'),
        ),
        migrations.AddField(
            model_name='curso',
            name='suscriptores',
            field=models.ManyToManyField(blank=True, related_name='Suscriptores', to='app.usuario'),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=500)),
                ('fecha', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('archivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.archivo', verbose_name='Archivo')),
                ('responde_a', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.comentario', verbose_name='Responde a')),
            ],
        ),
        migrations.AddField(
            model_name='archivo',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.curso', verbose_name='Curso'),
        ),
    ]
