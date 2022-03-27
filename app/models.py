from tabnanny import verbose
from django.db import models
from enum import Enum
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest
from django.utils.translation import gettext_lazy as _
from pytest import param
from django.contrib.auth.models import User
import psutil
from decouple import config

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


class PayPalClient:
    def __init__(self):
        self.client_id = config('PAYPAL_CLIENT_ID')
        self.client_secret = config('PAYPAL_SECRET_ID')

        

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        result = {}
        
        itr = json_data.__dict__.items()
        for key,value in itr:
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)


## Obtener los detalles de la transacción
class GetOrder(PayPalClient):

   
  def get_order(self, order_id):
    request = OrdersGetRequest(order_id)
    response = self.client.execute(request)
    return response
   


class CaptureOrder(PayPalClient):


  def capture_order(self, order_id, debug=False):
    request = OrdersCaptureRequest(order_id)
    response = self.client.execute(request)
    if debug:
      print ('Status Code: ', response.status_code)
      print ('Status: ', response.result.status)
      print ('Order ID: ', response.result.id)
      print ('Links: ')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      print ('Capture Ids: ')
      for purchase_unit in response.result.purchase_units:
        for capture in purchase_unit.payments.captures:
          print ('\t', capture.id)
      print ("Buyer:")
    return response