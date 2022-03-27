from tabnanny import verbose
from django.db import models
from enum import Enum
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from pytest import param
from django.contrib.auth.models import User
import psutil

def emails_distintos(email_academico):
    if('@alum.us.es' in email_academico):
        raise ValidationError(
            _('Los dos emails pertenecen a la Universidad de Sevilla'),
            params={'email_academico':email_academico}
        )

def validador_email(email):
    if('@alum.us.es' not in email):
        raise ValidationError(
            _('Este %(email)s no pertenece a la Universidad de Sevilla'),
            params={'email':email}
        )

def validador_archivo(file):
    if(file.size > 1024*1024*20):
        raise ValidationError(_('El archivo es demasiado grande'), code='mensaje')
    if(psutil.virtual_memory()[1] < 1024 * 1024 * 40):
        raise ValidationError(_('No hay memoria suficiente para subir el archivo, conctacte con el soporte técnico'), code='mensaje2')
        

class Asignatura(models.Model):
    nombre = models.CharField(max_length = 200)
    titulacion = models.CharField(max_length = 200)
    anyo = models.SmallIntegerField()

def image_directory_path(instance, filename):
    return 'user_images/{0}.jpg'.format(instance.django_user)

class Usuario(models.Model):
    email_academico = models.EmailField(primary_key=True, unique=True, validators=[validador_email])
    titulacion = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField(null=True, blank=True, upload_to=image_directory_path)
    dinero = models.DecimalField(max_digits=12, decimal_places=2)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="usuario", null=True)


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    fecha_publicacion = models.DateField()
    asignatura = models.ForeignKey(Asignatura, verbose_name="Asignatura", on_delete=models.DO_NOTHING)
    propietario = models.ForeignKey(Usuario, related_name="Propietario", on_delete=models.DO_NOTHING)
    suscriptores = models.ManyToManyField(Usuario, related_name="Suscriptores")

def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.curso.id, filename)
    
class Archivo(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_publicacion = models.DateField(auto_now_add=True, blank=True)
    curso = models.ForeignKey(Curso, verbose_name="Curso", on_delete=models.CASCADE)
    ruta = models.FileField(upload_to=user_directory_path, validators=[validador_archivo])


class Comentario(models.Model):
    texto = models.CharField(max_length=500)
    fecha = models.DateField()
    archivo = models.ForeignKey(Archivo, verbose_name="Archivo", on_delete=models.CASCADE)
    responde_a =  models.OneToOneField('self', null = True, blank = True, verbose_name = "Responde a", on_delete= models.DO_NOTHING)

    
class Notificacion(models.Model):
    class TipoNotificacion(models.TextChoices):
        COMENTARIO = "COMENTARIO"
        REPORTE = "REPORTE"
        NUEVO_ALUMNO = "NUEVO_ALUMNO"
        
    id_refencia = models.SmallIntegerField(null=True)
    tipo = models.CharField(max_length=20, choices=TipoNotificacion.choices)
    fecha = models.DateField()
    visto = models.BooleanField()
    usuario = models.ForeignKey(Usuario, verbose_name="Usuario", on_delete=models.CASCADE)


class Valoracion(models.Model):
    puntuacion = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    usuario = models.ForeignKey(Usuario, verbose_name="Usuario", on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, verbose_name="Curso", on_delete=models.CASCADE)

    
class Reporte(models.Model):
    class TipoReporte(models.TextChoices):
        PLAGIO = "PLAGIO"
        ERROR = "ERROR"
        
    descripcion = models.CharField(max_length=500)
    fecha = models.DateField()
    tipo = models.CharField(max_length=10, choices=TipoReporte.choices)