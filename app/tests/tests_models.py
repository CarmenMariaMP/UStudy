from email import charset
from sqlite3 import Date
from string import punctuation
from django.test import TestCase
from app.models import Asignatura,Archivo,Curso,Comentario,Notificacion,Valoracion,Usuario,Reporte,User
import decimal
from django.core.exceptions import ValidationError
import datetime
from datetime import timezone

## Estrategia: crear una clase por cada modelo
## Ejemplo: class AsignaturaModelTest(TestCase):
## es importante que herede de TestCase
## Para saber más sobre la estrategia elegida visitar el siguiente link:
## https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Testing


    
class AsignaturaModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        
    def test_crear_asignatura_positiva(self):

        asignatura=Asignatura.objects.first()
        self.assertEquals(asignatura.nombre,'Nombre1')
        self.assertEquals(asignatura.titulacion,'Titulacion1')
        self.assertEquals(asignatura.anyo,2012)
           


    def test_crear_asignatura_nombre_negativa(self):
        try:
            Asignatura.objects.create(nombre='a'*201, titulacion='Titulacion1', anyo=2012)
        except Exception as e:
            self.assertTrue(e.args[0] == "el valor es demasiado largo para el tipo character varying(200)\n" or
            e.args[0]=="value too long for type character varying(200)\n")

    def test_crear_asignatura_titulacion_negativa(self):
        try:
            Asignatura.objects.create(nombre='Nombre2', titulacion='a'*201, anyo=2012)
        except Exception as e:
            self.assertTrue(e.args[0] == "el valor es demasiado largo para el tipo character varying(200)\n" or
            e.args[0] == "value too long for type character varying(200)\n")
    
    def test_crear_asignatura_anyo_negativo(self):
        try:
            Asignatura.objects.create(nombre='Nombre3', titulacion='Titulacion3', anyo=60000)
        except Exception as e:
            self.assertTrue(e.args[0] == "smallint fuera de rango\n" or e.args[0]=="smallint out of range\n")

    def test_crear_asignatura_nombre_vacio(self):
        try:
            Asignatura.objects.create(nombre=None, titulacion='Titulacion3', anyo=2020)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «nombre» de la relación «app_asignatura» viola la restricción de no nulo" in e.args[0]
            or 'null value in column "nombre" of relation "app_asignatura" violates not-null constraint' in e.args[0])

    def test_crear_asignatura_titulacion_vacia(self):
        try:
            Asignatura.objects.create(nombre='Nombre5', titulacion=None, anyo=2020)
        except Exception as e:
            print(e.args[0])
            self.assertTrue("el valor nulo en la columna «titulacion» de la relación «app_asignatura» viola la restricción de no nulo" in e.args[0] or
            'null value in column "titulacion" of relation "app_asignatura" violates not-null constraint' in e.args[0])

    def test_crear_asignatura_anyo_vacio(self):
        try:
            Asignatura.objects.create(nombre='Nombre6', titulacion='Titulacion6', anyo=None)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «anyo» de la relación «app_asignatura» viola la restricción de no nulo" in e.args[0] or
            'null value in column "anyo" of relation "app_asignatura" violates not-null constraint' in e.args[0])

    def test_crear_asignatura_anyo_string(self):
        try:
            Asignatura.objects.create(nombre='Nombre7', titulacion='Titulacion7', anyo='')
        except Exception as e:
            self.assertTrue("Field 'anyo' expected a number but got ''" in e.args[0])

class UsuarioModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='User1', password='pass')
        
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
        self.assertTrue('el valor es demasiado largo para el tipo character varying(40)' in str(context.exception) or 
        "value too long for type character varying(40)" in str(context.exception))

    ## Longitud de apellido mayor de 40 caracteres
    def test_crear_usuario_negative_apellidos_longitud_max (self):
        user=User.objects.first()
        with self.assertRaises(Exception) as context:
            usuario = Usuario.objects.create(nombre='Nombre', apellidos='a'*41, email='email@hotmail.com', titulacion='Titulación 1',descripcion='Descripcion 1', 
            foto='foto.jpg', dinero=12.4, django_user=user)
        self.assertTrue('el valor es demasiado largo para el tipo character varying(40)' in str(context.exception) or 
         "value too long for type character varying(40)" in str(context.exception))

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
        #Instanciar objetos sin modificar que se usan en todos los métodos
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
            self.assertTrue("el valor nulo en la columna «fecha» de la relación «app_notificacion» viola la restricción de no nulo" in e.args[0] or
            'null value in column "fecha" of relation "app_notificacion" violates not-null constraint' in e.args[0])
    
    def test_crear_notificacion_visto_vacio(self):
        usuario = Usuario.objects.first()
        try:
            Notificacion.objects.create(tipo=Notificacion.TipoNotificacion["COMENTARIO"], fecha='2020-01-01', visto=None, usuario=usuario)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «visto» de la relación «app_notificacion» viola la restricción de no nulo" in e.args[0] or
             'null value in column "visto" of relation "app_notificacion" violates not-null constraint' in e.args[0])
            
    def test_crear_notificacion_usuario_vacio(self):
        try:
            Notificacion.objects.create(tipo=Notificacion.TipoNotificacion["COMENTARIO"], fecha='2020-01-01', visto=False, usuario=None)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «usuario_id» de la relación «app_notificacion» viola la restricción de no nulo" in e.args[0] or
             'null value in column "usuario_id" of relation "app_notificacion" violates not-null constraint' in e.args[0])
            
    def test_crear_notificacion_tipo_vacio(self):
        usuario = Usuario.objects.first()
        try:
            Notificacion.objects.create(tipo=None, fecha='2020-01-01', visto=False, usuario=usuario)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «tipo» de la relación «app_notificacion» viola la restricción de no nulo" in e.args[0] or
             'null value in column "tipo" of relation "app_notificacion" violates not-null constraint' in e.args[0])


    def test_crear_notificacion_negativa(self):
        usuario = Usuario.objects.first()
        notificacion = Notificacion.objects.create(tipo="", fecha='2020-01-01', visto=False, usuario=usuario)
        with self.assertRaises(Exception) as context:
            self.assertTrue(context.exception == {'id_refencia': ['This field cannot be blank.'], 'tipo': ['This field cannot be blank.']})
            notificacion.full_clean()

class ValoracionModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='nombreUsuario1', password='password1')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos1', email='nombreMail@gmail.com', 
                               email_academico='nombreMail@alum.us.es', titulacion='Titulacion1', descripcion='Descripcion1', 
                               foto=None, dinero=10.0, django_user=user)
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), asignatura=asignatura, propietario=usuario)
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

    def test_crear_valoracion_usuario_vacio(self):
        curso = Curso.objects.first()
    
        try:
            Valoracion.objects.create(puntuacion=6, usuario=None, curso=curso)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «usuario_id» de la relación «app_valoracion» viola la restricción de no nulo" in e.args[0] or
            'null value in column "usuario_id" of relation "app_valoracion" violates not-null constraint' in e.args[0])
    
    def test_crear_valoracion_curso_vacio(self):
        usuario = Usuario.objects.first()
        curso = Curso.objects.first()
        
        try:
            Valoracion.objects.create(puntuacion=None, usuario=usuario, curso=curso)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «puntuacion» de la relación «app_valoracion» viola la restricción de no nulo" in e.args[0] or 
            'null value in column "puntuacion" of relation "app_valoracion" violates not-null constraint' in e.args[0])

    def test_crear_valoracion_puntuacion_vacia(self):
        usuario = Usuario.objects.first()
        
        try:
            Valoracion.objects.create(puntuacion=6, usuario=usuario, curso=None)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «curso_id» de la relación «app_valoracion» viola la restricción de no nulo" in e.args[0] or
            'null value in column "curso_id" of relation "app_valoracion" violates not-null constraint' in e.args[0])

class CursoModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Instanciar objetos sin modificar que se usan en todos los métodos
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
        self.assertTrue('el valor es demasiado largo para el tipo character varying(100)' in str(context.exception) or
        'value too long for type character varying(100)' in str(context.exception))


    ## Longitud de descripcion mayor de 500 caracteres
    def test_crear_curso_negative_descripcion_longitud_max (self):
        user=User.objects.first()
        with self.assertRaises(Exception) as context:
            fecha = datetime.datetime.now().date()
            Curso.objects.create(nombre="Curso1", descripcion="a"*501, fecha_publicacion=fecha, asignatura=Asignatura.objects.first(), propietario=Usuario.objects.first())
        self.assertTrue('el valor es demasiado largo para el tipo character varying(500)' in str(context.exception) or
        "value too long for type character varying(500)" in str(context.exception))

class ComentarioModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        fecha = datetime.datetime.now().date()
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', email_academico='barranco@alum.us.es', titulacion='Titulación 1',descripcion='Descripcion 1', 
        foto='foto.jpg', dinero=12.4, django_user=user)
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=fecha, asignatura=asignatura, propietario=usuario)
        Archivo.objects.create(nombre='Archivo1', fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), curso=curso, ruta='ruta.pdf')
    
    def test_crear_comentario_positiva(self):
        fecha = datetime.datetime.now().replace(tzinfo=timezone.utc)
        Comentario.objects.create(texto='Texto1',fecha=fecha,archivo=Archivo.objects.first())

        comentario = Comentario.objects.first()
        self.assertEquals(comentario.texto,'Texto1')
        self.assertEquals(comentario.fecha,fecha)
        self.assertEquals(comentario.archivo,Archivo.objects.first())

    ## Longitud de texto mayor de 500 caracteres
    def test_crear_comentario_negative_texto_longitud_max(self):

        with self.assertRaises(Exception) as context:
            fecha = datetime.datetime.now().replace(tzinfo=timezone.utc)
            Comentario.objects.create(texto='a'*501,fecha=fecha,archivo=Archivo.objects.first())
        self.assertTrue('el valor es demasiado largo para el tipo character varying(500)' in str(context.exception) or
        "value too long for type character varying(500)" in str(context.exception))

class ArchivoModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        fecha = datetime.datetime.now().date()
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', email_academico='barranco@alum.us.es', titulacion='Titulación 1',descripcion='Descripcion 1', 
        foto='foto.jpg', dinero=12.4, django_user=user)
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=fecha, asignatura=asignatura, propietario=usuario)
        
    
    def test_crear_archivo_positiva(self):
        fecha = datetime.datetime.now().replace(tzinfo=timezone.utc)
        Archivo.objects.create(nombre='Archivo1', fecha_publicacion=fecha, curso=Curso.objects.first(), ruta='ruta.pdf')
        archivo = Archivo.objects.first()
        self.assertEquals(archivo.nombre,'Archivo1')
        self.assertEquals(archivo.fecha_publicacion,fecha)
        self.assertEquals(archivo.curso,Curso.objects.first())
        self.assertEquals(archivo.ruta,'ruta.pdf')

    ## Longitud de texto mayor de 200 caracteres
    def test_crear_comentario_negative_texto_longitud_max(self):
        with self.assertRaises(Exception) as context:
            fecha = datetime.datetime.now().replace(tzinfo=timezone.utc)
            Archivo.objects.create(nombre='a'*201, fecha_publicacion=fecha, curso=Curso.objects.first(), ruta='ruta.pdf')
        self.assertTrue('el valor es demasiado largo para el tipo character varying(200)' in str(context.exception))

class ReporteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Instanciar objetos sin modificar que se usan en todos los métodos        
        user = User.objects.create(username='nombreUsuario', password='password')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos1', email='nombreMail@gmail.com', 
                               email_academico='nombreMail@alum.us.es', titulacion='Titulacion1', descripcion='Descripcion1', 
                               foto=None, dinero=10.0, django_user=user)  
        
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime(2022, 3, 29, 0, 0, 0).replace(tzinfo=timezone.utc), asignatura=asignatura, propietario=usuario)
        archivo = Archivo.objects.create(nombre="Archivo1", fecha_publicacion=datetime.datetime(2022, 3, 29, 0, 0, 0).replace(tzinfo=timezone.utc), curso=curso, ruta="ruta.pdf")
        
        Reporte.objects.create(descripcion="Descripcion1", fecha=datetime.datetime(2022, 3, 31, 0, 0, 0).replace(tzinfo=timezone.utc), tipo=Reporte.TipoReporte["PLAGIO"], usuario=usuario, archivo=archivo)
        
    def test_crear_reporte_positivo(self):
        usuario = Usuario.objects.first()
        archivo = Archivo.objects.first()
        reporte = Reporte.objects.get(id=1)
        fecha = datetime.datetime(2022, 3, 31, 0, 0, 0).replace(tzinfo=timezone.utc)
        self.assertEquals(reporte.descripcion, "Descripcion1")
        self.assertEquals(reporte.fecha, fecha)
        self.assertEquals(reporte.tipo, Reporte.TipoReporte["PLAGIO"])
        self.assertEquals(reporte.usuario, usuario)
        self.assertEquals(reporte.archivo, archivo)
        
    def test_crear_reporte_negativo_descripcion_longitud_max(self):
        try:
            Reporte.objects.create(descripcion='a'*501, fecha=datetime.datetime(2022, 3, 30, 0, 0, 0).replace(tzinfo=timezone.utc), tipo=Reporte.TipoReporte["PLAGIO"], usuario=Usuario.objects.first(), archivo=Archivo.objects.first())
        except Exception as e:
            self.assertTrue('el valor es demasiado largo para el tipo character varying(500)' in e.args[0])
            
    def test_crear_reporte_descripcion_vacia(self):
        try:
            Reporte.objects.create(descripcion=None, fecha=datetime.datetime(2022, 3, 30, 0, 0, 0).replace(tzinfo=timezone.utc), tipo=Reporte.TipoReporte["PLAGIO"], usuario=Usuario.objects.first(), archivo=Archivo.objects.first())
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «descripcion» de la relación «app_reporte» viola la restricción de no nulo" in e.args[0] or
             'null value in column "descripcion" of relation "app_reporte" violates not-null constraint' in e.args[0])
            
    def test_crear_reporte_fecha_vacia(self):
        try:
            Reporte.objects.create(descripcion="Descripcion1", fecha=None, tipo=Reporte.TipoReporte["PLAGIO"], usuario=Usuario.objects.first(), archivo=Archivo.objects.first())
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «fecha» de la relación «app_reporte» viola la restricción de no nulo" in e.args[0] or
             'null value in column "fecha" of relation "app_reporte" violates not-null constraint' in e.args[0])
            
    def test_crear_reporte_tipo_vacio(self):
        try:
            Reporte.objects.create(descripcion="Descripcion1", fecha=datetime.datetime(2022, 3, 30, 0, 0, 0).replace(tzinfo=timezone.utc), tipo=None, usuario=Usuario.objects.first(), archivo=Archivo.objects.first())
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «tipo» de la relación «app_reporte» viola la restricción de no nulo" in e.args[0] or
             'null value in column "tipo" of relation "app_reporte" violates not-null constraint' in e.args[0])
            
    def test_crear_reporte_usuario_vacio(self):
        try:
            Reporte.objects.create(descripcion="Descripcion1", fecha=datetime.datetime(2022, 3, 30, 0, 0, 0).replace(tzinfo=timezone.utc), tipo=Reporte.TipoReporte["PLAGIO"], usuario=None, archivo=Archivo.objects.first())
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «usuario_id» de la relación «app_reporte» viola la restricción de no nulo" in e.args[0] or
             'null value in column "usuario_id"  of relation "app_reporte" violates not-null constraint' in e.args[0])
            
    def test_crear_reporte_archivo_vacio(self):
        try:
            Reporte.objects.create(descripcion="Descripcion1", fecha=datetime.datetime(2022, 3, 30, 0, 0, 0).replace(tzinfo=timezone.utc), tipo=Reporte.TipoReporte["PLAGIO"], usuario=Usuario.objects.first(), archivo=None)
        except Exception as e:
            self.assertTrue("el valor nulo en la columna «archivo_id» de la relación «app_reporte» viola la restricción de no nulo" in e.args[0] or
            'null value in column "archivo_id"  of relation "app_reporte" violates not-null constraint' in e.args[0])
            
    