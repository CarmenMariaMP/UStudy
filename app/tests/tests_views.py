from django.test import TestCase, Client
from app.models import User,Usuario,Curso,Asignatura,Archivo
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

class LoginViewTests(TestCase):

    @classmethod
    def setUp(self):
        #Instanciar objetos sin modificar que se usan en todos los métodos
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', email_academico='barranco@alum.us.es', titulacion='Titulación 1',descripcion='Descripcion 1', 
        foto='foto.jpg', dinero=9.53, django_user=user)

    # muestra vista de login al hacer consulta get
    def test_login_view(self):
        #TODO
        pass

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
        user = User.objects.create(username='User1', password='pass')
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com', 
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        
        
    def test_create_course_view(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/crearcurso', follow=True)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'crearcurso.html')
        
    '''
    def test_create_course_post_view(self):
        client = Client()
        client.force_login(User.objects.first())
        response = client.get('/crearcurso', follow=True)
        response = client.post('/crearcurso/', data={"nombre": "Curso de prueba", "descripcion": "Esto es una descripción de prueba", "asignatura": "1"})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'inicio_profesor.html')
    '''
    
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
        
