from tabnanny import verbose
from django.db import models
from enum import Enum
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from pytest import param

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

class Asignatura(models.Model):
    nombre = models.CharField(max_length = 200)
    titulacion = models.CharField(max_length = 200)
    anyo = models.SmallIntegerField()


class Usuario(models.Model):
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    email_academico = models.EmailField(primary_key=True, unique=True, validators=[validador_email])
    titulacion = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    foto = models.CharField(max_length=100)
    contrasenha = models.CharField(max_length=100)
    dinero = models.DecimalField(max_digits=12, decimal_places=2)


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    fecha_publicacion = models.DateField()
    asignatura = models.ForeignKey(Asignatura, verbose_name="Asignatura", on_delete=models.DO_NOTHING)
    propietario = models.ForeignKey(Usuario, related_name="Propietario", on_delete=models.DO_NOTHING)
    suscriptores = models.ManyToManyField(Usuario, related_name="Suscriptores")

    
class Archivo(models.Model):
    nombre = models.CharField(max_length=200)
    ruta = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()
    curso = models.ForeignKey(Curso, verbose_name="Curso", on_delete=models.CASCADE)


class Comentario(models.Model):
    texto = models.CharField(max_length=500)
    fecha = models.DateField()
    archivo = models.ForeignKey(Archivo, verbose_name="Archivo", on_delete=models.CASCADE)
    responde_a =  models.OneToOneField('self', null = True, blank = True, verbose_name = "Responde a", on_delete= models.DO_NOTHING)
     
    
class Notificacion(models.Model):
    fecha = models.DateField()
    visto = models.BooleanField()
    usuario = models.ForeignKey(Usuario, verbose_name="Usuario", on_delete=models.CASCADE)
    comentario = models.ForeignKey(Comentario, verbose_name="Comentario", on_delete=models.CASCADE)


class Valoracion(models.Model):
    puntuacion = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    usuario = models.ForeignKey(Usuario, verbose_name="Usuario", on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, verbose_name="Curso", on_delete=models.CASCADE)


class TipoReporte(Enum):
    PLAGIO = "PLAGIO"
    ERROR = "ERROR"
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    
class Reporte(models.Model):
    descripcion = models.CharField(max_length=500)
    
    fecha = models.DateField()
    class TipoReporte(models.TextChoices):
        PLAGIO = "PLAGIO"
        ERROR = "ERROR"

    tipo_reporte = models.CharField(max_length=10, choices=TipoReporte.choices)