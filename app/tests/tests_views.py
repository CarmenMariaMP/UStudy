from django.test import TestCase, Client
from app.models import User,Usuario
import json

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
        