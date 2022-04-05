from django.test import TestCase, Client
from app.models import Reporte, User,Usuario,Curso,Asignatura,Archivo
import json
import datetime
from datetime import timezone


class InicioViewTests(TestCase):

    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', email_academico='barranco@alum.us.es', titulacion='Titulación 1',descripcion='Descripcion 1', 
        foto='foto.jpg', dinero=9.53, django_user=user)

    # envia a la vista de login si el usuario no se ha autenticado
    def test_not_logged(self):
        client = Client()
        response = client.get('/')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'inicio.html')

    # envia a la vista de sus cursos si el usuario esta autenticado
    def test_logged(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'miscursos.html')

class PerfilUsuarioViewTests(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
    def test_profile_view(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/perfil', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'perfil.html')
        
    def test_profile_view_not_logged(self):
        client = Client()
        response = client.get('/perfil', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'login.html')
        
class InicioProfesotViewTests(TestCase):
        
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
    def test_profesor_view(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/inicio_profesor', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'inicio_profesor.html')
        
    def test_profesor_view_not_logged(self):
        client = Client()
        response = client.get('/inicio_profesor', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'login.html')

class CrearCursoViewTests(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulacion1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
        
    def test_create_course_view(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/crearcurso', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'crearcurso.html')
        

    def test_create_course_post_view(self):
        
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/crearcurso', follow=True)
        response = client.post('/crearcurso/', data={"nombre": "Curso de prueba", "descripcion": "Esto es una descripción de prueba", "asignatura": Asignatura.objects.first().id})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response,'/inicio_profesor',fetch_redirect_response=False)
    
    
    def test_create_course_view_not_logged(self):
        client = Client()
        response = client.get('/crearcurso', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'inicio.html')   

class CursosDisponiblesViewTests(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
        
    def test_courses_available_view(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/cursosdisponibles', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'cursosdisponibles.html')
        
    
    def test_create_course_available_view_not_logged(self):
        client = Client()
        response = client.get('/cursosdisponibles', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'login.html')
     
class MisCursosViewTests(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
        
    def test_my_courses_view(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/miscursos', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'miscursos.html')
        
    
    def test_my_courses_view_not_logged(self):
        client = Client()
        response = client.get('/miscursos', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'login.html')
        
class CursoViewTests(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
        
        user2 = User.objects.create(username='User2', password='pass')
        usuario2 = Usuario.objects.create(nombre='Nombre2', apellidos='Apellidos', email='email2@hotmail.com', 
                                         email_academico='barranco2@alum.us.es', titulacion='Titulacion1',
                                         descripcion='Descripcion 2', foto='foto2.jpg', dinero=9.53, django_user=user2)
        
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), asignatura=asignatura, propietario=usuario)
        
    def test_course_view(self):
        client = Client()
        client.force_login(User.objects.get(username='User2'))
        curso_id = Curso.objects.first().id
        response = client.get('/curso/'+str(curso_id), follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'curso.html')
        
    def test_course_view_not_same_titulation(self):
        client = Client()
        client.force_login(User.objects.first())
        curso_id = Curso.objects.first().id
        response = client.get('/curso/'+str(curso_id), follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'cursosdisponibles.html')        
    
    def test_course_view_not_logged(self):
        client = Client()
        curso_id = Curso.objects.first().id
        response = client.get('/curso/'+str(curso_id), follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'inicio.html')
        
class ArchivoViewTests(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
        
        user2 = User.objects.create(username='User2', password='pass')
        usuario2 = Usuario.objects.create(nombre='Nombre2', apellidos='Apellidos', email='email2@hotmail.com', 
                                         email_academico='barranco2@alum.us.es', titulacion='Titulacion1',
                                         descripcion='Descripcion 2', foto='foto2.jpg', dinero=9.53, django_user=user2)
        
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), asignatura=asignatura, propietario=usuario)
        archivo = Archivo.objects.create(nombre='Archivo1', fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), curso=curso, ruta='ruta.pdf')
        
    def test_file_view(self):
        client = Client()
        client.force_login(User.objects.get(username='User2'))
        curso_id = Curso.objects.first().id
        archivo_id = Archivo.objects.first().id
        response = client.get('/curso/'+str(curso_id)+"/archivo/"+str(archivo_id), follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'archivo.html')
        
    
    def test_file_view_not_logged(self):
        client = Client()
        curso_id = Curso.objects.first().id
        response = client.get('/curso/'+str(curso_id), follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'inicio.html')
        
class LogoutTestView(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
    def test_logout_view_test(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/logout/', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'inicio.html')
    
class LoginTestView(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1')
        user.set_password('pass')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
    def test_login_view_test_logged(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/login/', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'miscursos.html')
    
    def test_login_view_test_not_logged(self):
        client = Client()
        response = client.get('/login/', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_view_test_not_logged_to_logged(self):
        client = Client()
        response = client.post('/login/', data={"username": "User1", "contrasena": "pass"}, follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'miscursos.html')

class borrarArchivoTestView(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        fecha = datetime.datetime.now().date()
        user = User.objects.create(username='User1')
        user.set_password('pass')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulacion1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=fecha, asignatura=asignatura, propietario=usuario)
        Archivo.objects.create(nombre='Archivo1', fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), curso=curso, ruta='ruta.pdf')
        
    def test_borrar_archivo_positive(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/curso/'+str(Curso.objects.first().id)+'/'+str(Archivo.objects.first().id), follow=True)
        self.assertEquals(response.status_code,200)
        self.assertRedirects(response,'/curso/'+str(Curso.objects.first().id),fetch_redirect_response=False)
    
class ValorarCursoTestView(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1')
        user.set_password('pass')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
        
        user2 = User.objects.create(username='User2', password='pass')
        usuario2 = Usuario.objects.create(nombre='Nombre2', apellidos='Apellidos', email='email2@hotmail.com', 
                                         email_academico='barranco2@alum.us.es', titulacion='Titulacion1',
                                         descripcion='Descripcion 2', foto='foto2.jpg', dinero=9.53, django_user=user2)
        
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), asignatura=asignatura, propietario=usuario)
        archivo = Archivo.objects.create(nombre='Archivo1', fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), curso=curso, ruta='ruta.pdf')
        
        
    def test_rate_file_view(self):
        client = Client()
        client.force_login(User.objects.get(username='User2'))
        curso_id = Curso.objects.first().id
        response = client.post('/valorar_curso/', data={"id": str(curso_id), "valoracion": "5"}, follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTrue(response.content == b'{"succes": "true", "score": "5"}')
        
class EditarCursoTestView(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1')
        user.set_password('pass')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
        
        user2 = User.objects.create(username='User2')
        user.set_password('pass')
        user.save()
        usuario2 = Usuario.objects.create(nombre='Nombre2', apellidos='Apellidos', email='email2@hotmail.com', 
                                         email_academico='barranco2@alum.us.es', titulacion='Titulacion1',
                                         descripcion='Descripcion 2', foto='foto2.jpg', dinero=9.53, django_user=user2)
        
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), asignatura=asignatura, propietario=usuario)
        
    def test_course_edit_view(self):
        client = Client()
        client.force_login(User.objects.get(username='User1'))
        curso_id = Curso.objects.first().id
        response = client.post('/editarcurso/'+str(curso_id), data={"nombre": "Nuevo nombre", "descripcion": "Nueva descripcion"}, follow=True)
        self.assertEquals(response.status_code,200)
        self.assertRedirects(response,'/inicio_profesor/',fetch_redirect_response=False)
        
    def test_course_edit_view_bad_form(self):
        client = Client()
        client.force_login(User.objects.get(username='User1'))
        curso_id = Curso.objects.first().id
        response = client.post('/editarcurso/'+str(curso_id), data={"nombres": "Nuevo nombre", "descripcion": "Nueva descripcion"}, follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'editarcurso.html')
        
    def test_course_edit_view_get(self):
        client = Client()
        client.force_login(User.objects.get(username='User1'))
        curso_id = Curso.objects.first().id
        response = client.get('/editarcurso/'+str(curso_id), follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'editarcurso.html')
        
    def test_course_edit_view_another_owner(self):
        client = Client()
        client.force_login(User.objects.get(username='User2'))
        curso_id = Curso.objects.first().id
        response = client.post('/editarcurso/'+str(curso_id), data={"nombres": "Nuevo nombre", "descripcion": "Nueva descripcion"}, follow=True)
        self.assertEquals(response.status_code,200)
        self.assertRedirects(response,'/miscursos/',fetch_redirect_response=False)
        
    def test_course_edit_view_not_logged(self):
        client = Client()
        curso_id = Curso.objects.first().id
        response = client.post('/editarcurso/'+str(curso_id), data={"nombres": "Nuevo nombre", "descripcion": "Nueva descripcion"}, follow=True)
        self.assertEquals(response.status_code,200)
        self.assertRedirects(response,'/login/',fetch_redirect_response=False)

class borrarReporteTestView(TestCase):
    
    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        fecha = datetime.datetime.now().date()
        user = User.objects.create(username='User1')
        user.set_password('pass')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulacion1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        asignatura = Asignatura.objects.create(nombre='Nombre1', titulacion='Titulacion1', anyo=2012)
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=fecha, asignatura=asignatura, propietario=usuario)
        archivo = Archivo.objects.create(nombre='Archivo1', fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), curso=curso, ruta='ruta.pdf')
        Reporte.objects.create(descripcion="Descripcion1", fecha=datetime.datetime.now().replace(tzinfo=timezone.utc), tipo=Reporte.TipoReporte["PLAGIO"], usuario=usuario, archivo=archivo)

        
    def test_borrar_reporte_positive(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/curso/'+str(Curso.objects.first().id)+'/archivo/'+str(Archivo.objects.first().id)+'/reporte/'+str(Reporte.objects.first().id), follow=True)
        self.assertEquals(response.status_code,200)
        self.assertRedirects(response,'/curso/'+str(Curso.objects.first().id)+'/archivo/'+str(Archivo.objects.first().id),fetch_redirect_response=False)
        
class SubirContenidoTestView(TestCase):
    
    def test_upload_content_test(self):
        client = Client()
        self.assertTemplateUsed(client.get('/subir_contenido/'), 'subir_contenido.html')
        
class ErrorsTestView(TestCase):
    
    def test_error_404(self):
        client = Client()
        response = client.get('/error404/')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'error.html')
        
    def test_error_403(self):
        # TODO testear error 403
        pass 
        
    def test_error_500(self):
        # TODO testear error 500
        pass

class RegistroTestView(TestCase):
    
    def test_register_view_get(self):
        client = Client()
        response = client.get('/registro/')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'registro.html')
    
    def test_register_view_post(self):
        client = Client()
        data_form = {
            "password": "passwd", 
            "confirm_password": "passwd", 
            "usename": "nomapedos", 
            "name": "Nombre", 
            "surname": "Apellidos", 
            "email": "email@gmail.com", 
            "email_academico": "email@alum.us.es", 
            "titulacion": "Titulacion1", 
            "descripcion": "descripcion", 
            "dinero": "0.0"
        }
        response = client.post('/registro/', data=data_form, follow=True)
        self.assertEquals(response.status_code,200)
        #self.assertRedirects(response,'/login/',fetch_redirect_response=False) # TODO: Comprobar que redirige a login
        
    def test_register_view_post_different_passwords(self):
        client = Client()
        data_form = {
            "password": "passwd", 
            "confirm_password": "passwd1", 
            "usename": "nomapedos", 
            "name": "Nombre", 
            "surname": "Apellidos", 
            "email": "email@gmail.com", 
            "email_academico": "email@alum.us.es", 
            "titulacion": "Titulacion1", 
            "descripcion": "descripcion", 
            "dinero": "0.0"
        }
        response = client.post('/registro/', data=data_form, follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'registro.html')