from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth.models import User
import psutil


def emails_distintos(email_academico):
    if('@alum.us.es' in email_academico):
        raise ValidationError(
            _('Los dos emails pertenecen a la Universidad de Sevilla'),
            params={'email_academico': email_academico}
        )


def validador_email(email):
    if('@alum.us.es' not in email):
        raise ValidationError(
            _('Este %(email)s no pertenece a la Universidad de Sevilla'),
            params={'email': email}
        )


def validador_archivo(file):
    if(file.size > 1024*1024*20):
        raise ValidationError(
            _('El tamaño del archivo debe ser inferior a 20 MB'), code='mensaje')
    if not file.name[-4:] in ('.pdf', '.mp4', '.png', '.jpg', '.txt', 'jpeg', '.PDF', '.MP4', '.PNG', '.JPG', '.TXT', '.JPEG'):
        raise ValidationError(
            _('El formato del archivo debe ser PDF, MP4, PNG, JPG, JPEG ó TXT'), code='mensaje3')
    if(psutil.virtual_memory()[1] < 1024 * 1024 * 40):
        raise ValidationError(
            _('No hay memoria suficiente para subir el archivo, contacte con el soporte técnico'), code='mensaje2')


class Asignatura(models.Model):
    nombre = models.CharField(max_length=200)
    titulacion = models.CharField(max_length=200)
    anyo = models.SmallIntegerField()


def image_directory_path(instance, filename):
    return '{0}.jpg'.format(instance.django_user)


class Usuario(models.Model):
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    email = models.EmailField(unique=True, max_length=254)
    email_academico = models.EmailField(
        primary_key=True, unique=True, validators=[validador_email])
    titulacion = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500, blank=True)
    foto = models.ImageField(null=True, blank=True,
                             upload_to=image_directory_path)
    dinero = models.DecimalField(max_digits=12, decimal_places=2)
    django_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="usuario", null=True)


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    fecha_publicacion = models.DateField()
    asignatura = models.ForeignKey(
        Asignatura, verbose_name="Asignatura", on_delete=models.DO_NOTHING)
    propietario = models.ForeignKey(
        Usuario, related_name="Propietario", on_delete=models.DO_NOTHING)
    suscriptores = models.ManyToManyField(
        Usuario, related_name="Suscriptores", blank=True)


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.curso.id, filename)


class Archivo(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField(default=now, blank=True)
    curso = models.ForeignKey(
        Curso, verbose_name="Curso", related_name = "archivos" ,on_delete=models.CASCADE)
    ruta = models.FileField(upload_to=user_directory_path,
                            validators=[validador_archivo])
                            

class Comentario(models.Model):
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField(default=now, blank=True)
    archivo = models.ForeignKey(
        Archivo, verbose_name="Archivo", on_delete=models.CASCADE)
    responde_a = models.ForeignKey(
        'self', null=True, blank=True, verbose_name="Responde a", on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Notificacion(models.Model):
    class TipoNotificacion(models.TextChoices):
        COMENTARIO = "COMENTARIO"
        REPORTE = "REPORTE"
        NUEVO_ALUMNO = "NUEVO_ALUMNO"
        RESENYA= "NUEVA RESEÑA"

    referencia = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TipoNotificacion.choices)
    fecha = models.DateTimeField(default=now, blank=True)
    visto = models.BooleanField()
    usuario = models.ForeignKey(
        Usuario, verbose_name="Usuario", on_delete=models.CASCADE)
    curso = models.ForeignKey(
        Curso, verbose_name="Curso", on_delete=models.CASCADE)
    alumno = models.ForeignKey(
        Usuario, related_name="alumno", on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.CharField(max_length=500, null=True, blank=True)


class Valoracion(models.Model):
    puntuacion = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    usuario = models.ForeignKey(
        Usuario, verbose_name="Usuario", on_delete=models.CASCADE)
    curso = models.ForeignKey(
        Curso, verbose_name="Curso", on_delete=models.CASCADE)

class Resenya(models.Model):
    descripcion = models.TextField(max_length=500)
    fecha = models.DateTimeField(default=now, blank=True)
    usuario = models.ForeignKey(
        Usuario, verbose_name="Usuario", on_delete=models.CASCADE)
    curso = models.ForeignKey(
        Curso, verbose_name="Curso", on_delete=models.CASCADE)

class Reporte(models.Model):
    class TipoReporte(models.TextChoices):
        PLAGIO = "PLAGIO"
        ERROR = "ERROR"
    descripcion = models.TextField(max_length=500)
    fecha = models.DateTimeField(default=now, blank=True)
    tipo = models.CharField(max_length=10, choices=TipoReporte.choices)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="usuario", null=True)
    archivo = models.ForeignKey(
        Archivo, on_delete=models.CASCADE, related_name="archivo", null=True)

class TicketDescarga(models.Model):
    usuario = models.ForeignKey(Usuario, related_name="Usuario", on_delete=models.CASCADE)
    archivo = models.ForeignKey(Archivo, related_name="Archivo", on_delete=models.CASCADE)

class RetiradaDinero(models.Model):
    email = models.EmailField(unique=True, max_length=254)
    dinero = models.DecimalField(max_digits=12, decimal_places=2)
