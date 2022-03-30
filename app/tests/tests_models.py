from sqlite3 import Date
from string import punctuation
from django.test import TestCase
from app.models import *
import decimal
import datetime

## Estrategia: crear una clase por cada modelo
## Ejemplo: class AsignaturaModelTest(TestCase):
## es importante que herede de TestCase
## Para saber más sobre la estrategia elegida visitar el siguiente link:
## https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Testing


    
class AsignaturaModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        
    def test_crear_asignatura_positiva(self):

        asignatura=Asignatura.objects.get(id=1)
        self.assertEquals(asignatura.nombre,'Nombre1')
        self.assertEquals(asignatura.titulacion,'Titulacion1')
        self.assertEquals(asignatura.anyo,2012)
           


    def test_crear_asignatura_nombre_negativa(self):
        try:
            Asignatura.objects.create(nombre='a'*201, titulacion='Titulacion1', anyo=2012)
        except Exception as e:
            self.assertTrue(e.args[0] == "el valor es demasiado largo para el tipo character varying(200)\n")

    def test_crear_asignatura_titulacion_negativa(self):
        try:
            Asignatura.objects.create(nombre='Nombre2', titulacion='a'*201, anyo=2012)
        except Exception as e:
            self.assertTrue(e.args[0] == "el valor es demasiado largo para el tipo character varying(200)\n")
    
    def test_crear_asignatura_anyo_negativo(self):
        try:
            Asignatura.objects.create(nombre='Nombre3', titulacion='Titulacion3', anyo=60000)
        except Exception as e:
            self.assertTrue(e.args[0] == "smallint fuera de rango\n")

    def test_crear_asignatura_nombre_vacio(self):
        try:
            Asignatura.objects.create(nombre=None, titulacion='Titulacion3', anyo=2020)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «nombre» de la relación «app_asignatura» viola la restricción de no nulo" in e.args[0])

    def test_crear_asignatura_titulacion_vacia(self):
        try:
            Asignatura.objects.create(nombre='Nombre5', titulacion=None, anyo=2020)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «titulacion» de la relación «app_asignatura» viola la restricción de no nulo" in e.args[0])

    def test_crear_asignatura_anyo_vacio(self):
        try:
            Asignatura.objects.create(nombre='Nombre6', titulacion='Titulacion6', anyo=None)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «anyo» de la relación «app_asignatura» viola la restricción de no nulo" in e.args[0])

    def test_crear_asignatura_anyo_string(self):
        try:
            Asignatura.objects.create(nombre='Nombre7', titulacion='Titulacion7', anyo='')
        except Exception as e:
            self.assertTrue("Field 'anyo' expected a number but got ''" in e.args[0])
    

class UsuarioModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='User1', password='pass')
        print(user)
        
    def test_crear_usuario_positive(self):
        user=User.objects.first()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', email_academico='barranco@alum.us.es', titulacion='Titulación 1',descripcion='Descripcion 1', 
        foto='foto.jpg', dinero=decimal.Decimal(9.53), django_user=user)

        self.assertEquals(usuario.nombre,'Nombre1')
        self.assertEquals(usuario.apellidos,'Apellidos')
        self.assertEquals(usuario.email,'email@hotmail.com')
        self.assertEquals(usuario.email_academico,'barranco@alum.us.es')
        self.assertEquals(usuario.titulacion,'Titulación 1')
        self.assertEquals(usuario.descripcion,'Descripcion 1')
        self.assertEquals(usuario.foto,'foto.jpg')
        self.assertEquals(usuario.dinero,decimal.Decimal(9.53))



    ## Longitud de nombre mayor de 40 caracteres
    def test_crear_usuario_negative_nombre_longitud_max (self):
        user=User.objects.first()
        with self.assertRaises(Exception) as context:
            usuario = Usuario.objects.create(nombre='a'*41, apellidos='Apellidos', email='email@hotmail.com', titulacion='Titulación 1',descripcion='Descripcion 1', 
            foto='foto.jpg', dinero=12.4, django_user=user)
        self.assertTrue('el valor es demasiado largo para el tipo character varying(40)' in str(context.exception))

    ## Longitud de apellido mayor de 40 caracteres
    def test_crear_usuario_negative_apellidos_longitud_max (self):
        user=User.objects.first()
        with self.assertRaises(Exception) as context:
            usuario = Usuario.objects.create(nombre='Nombre', apellidos='a'*41, email='email@hotmail.com', titulacion='Titulación 1',descripcion='Descripcion 1', 
            foto='foto.jpg', dinero=12.4, django_user=user)
        self.assertTrue('el valor es demasiado largo para el tipo character varying(40)' in str(context.exception))

    ## Email academico sin dominio de la US
    def test_email_academico_negative(self):
        user=User.objects.first()
        usuario = Usuario.objects.create(nombre='Nombre', apellidos='Apellidos', email='email@hotmail.com', email_academico='email@hotmail.com',titulacion='Titulación 1',descripcion='Descripcion 1', 
            foto='foto.jpg', dinero=12.42, django_user=user)

        with self.assertRaises(ValidationError) as context:
            usuario.full_clean()
        self.assertTrue('email_academico' in dict(context.exception))
            

class NotificacionModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='nombreUsuario', password='password')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos1', email='nombreMail@gmail.com', 
                               email_academico='nombreMail@alum.us.es', titulacion='Titulacion1', descripcion='Descripcion1', 
                               foto=None, dinero=10.0, django_user=user)
        Notificacion.objects.create(tipo=Notificacion.TipoNotificacion["COMENTARIO"], fecha='2020-01-01', visto=False, usuario=usuario)
        
    def test_crear_notificacion_positiva(self):
        usuario = Usuario.objects.first()
        notificacion = Notificacion.objects.get(id=1)
        self.assertEquals(notificacion.tipo,Notificacion.TipoNotificacion["COMENTARIO"])
        self.assertEquals(notificacion.fecha,datetime.date(2020, 1, 1))
        self.assertEquals(notificacion.visto,False)
        self.assertEquals(notificacion.usuario,usuario)
        
    def test_crear_notificacion_fecha_vacia(self):
        usuario = Usuario.objects.first()
        try:
            Notificacion.objects.create(tipo=Notificacion.TipoNotificacion["COMENTARIO"], fecha=None, visto=False, usuario=usuario)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «fecha» de la relación «app_notificacion» viola la restricción de no nulo" in e.args[0])
    
    def test_crear_notificacion_visto_vacio(self):
        usuario = Usuario.objects.first()
        try:
            Notificacion.objects.create(tipo=Notificacion.TipoNotificacion["COMENTARIO"], fecha='2020-01-01', visto=None, usuario=usuario)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «visto» de la relación «app_notificacion» viola la restricción de no nulo" in e.args[0])
            
    def test_crear_notificacion_usuario_vacio(self):
        try:
            Notificacion.objects.create(tipo=Notificacion.TipoNotificacion["COMENTARIO"], fecha='2020-01-01', visto=False, usuario=None)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «usuario_id» de la relación «app_notificacion» viola la restricción de no nulo" in e.args[0])
            
    def test_crear_notificacion_usuario_vacio(self):
        usuario = Usuario.objects.first()
        try:
            Notificacion.objects.create(tipo=None, fecha='2020-01-01', visto=False, usuario=usuario)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «tipo» de la relación «app_notificacion» viola la restricción de no nulo" in e.args[0])


    def test_crear_notificacion_negativa(self):
        usuario = Usuario.objects.first()
        notificacion = Notificacion.objects.create(tipo="", fecha='2020-01-01', visto=False, usuario=usuario)
        with self.assertRaises(Exception) as context:
            self.assertTrue(context.exception == {'id_refencia': ['This field cannot be blank.'], 'tipo': ['This field cannot be blank.']})
            notificacion.full_clean()
        print("EXCEPTION",context.exception)

class ValoracionModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='nombreUsuario1', password='password1')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos1', email='nombreMail@gmail.com', 
                               email_academico='nombreMail@alum.us.es', titulacion='Titulacion1', descripcion='Descripcion1', 
                               foto=None, dinero=10.0, django_user=user)
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime.now(), asignatura=asignatura, propietario=usuario)
        Valoracion.objects.create(puntuacion=5, usuario=usuario, curso=curso)
        
    def test_crear_valoracion_positiva(self):
        valoracion = Valoracion.objects.first()
        usuario = Usuario.objects.first()
        curso = Curso.objects.first()
        self.assertEquals(valoracion.puntuacion,5)
        self.assertEquals(valoracion.usuario,usuario)
        self.assertEquals(valoracion.curso,curso)

    def test_crear_valoracion_negativa_puntuacion(self):
        usuario = Usuario.objects.first()
        curso = Curso.objects.first()
        
        valoracion = Valoracion.objects.create(puntuacion=6, usuario=usuario, curso=curso)
        with self.assertRaises(Exception) as context:
            self.assertTrue(context.exception == {'puntuacion': ['Ensure this value is less than or equal to 5.']})
            valoracion.full_clean()
        
        valoracion = Valoracion.objects.create(puntuacion=0, usuario=usuario, curso=curso)
        with self.assertRaises(Exception) as context:
            self.assertTrue(context.exception == {'puntuacion': ['Ensure this value is greater than or equal to 1.']})
            valoracion.full_clean()

class CursoModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', email_academico='barranco@alum.us.es', titulacion='Titulación 1',descripcion='Descripcion 1', 
        foto='foto.jpg', dinero=12.4, django_user=user)
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
    
    def test_crear_curso_positiva(self):
        fecha = datetime.datetime.now().date()
        Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=fecha, asignatura=Asignatura.objects.first(), propietario=Usuario.objects.first())

        curso = Curso.objects.first()
        self.assertEquals(curso.nombre,"Curso1")
        self.assertEquals(curso.descripcion,"Descripcion1")
        self.assertEquals(curso.fecha_publicacion,fecha)
        self.assertEquals(curso.asignatura,Asignatura.objects.first())
        self.assertEquals(curso.propietario,Usuario.objects.first())

    ## Longitud de nombre mayor de 100 caracteres
    def test_crear_curso_negative_nombre_longitud_max (self):
        user=User.objects.first()
        with self.assertRaises(Exception) as context:
            fecha = datetime.datetime.now().date()
            Curso.objects.create(nombre="a"*101, descripcion="Descripcion1", fecha_publicacion=fecha, asignatura=Asignatura.objects.first(), propietario=Usuario.objects.first())
        self.assertTrue('el valor es demasiado largo para el tipo character varying(100)' in str(context.exception))


    ## Longitud de descripcion mayor de 500 caracteres
    def test_crear_curso_negative_descripcion_longitud_max (self):
        user=User.objects.first()
        with self.assertRaises(Exception) as context:
            fecha = datetime.datetime.now().date()
            Curso.objects.create(nombre="Curso1", descripcion="a"*501, fecha_publicacion=fecha, asignatura=Asignatura.objects.first(), propietario=Usuario.objects.first())
        self.assertTrue('el valor es demasiado largo para el tipo character varying(500)' in str(context.exception))
