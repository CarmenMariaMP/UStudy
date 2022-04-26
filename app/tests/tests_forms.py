from django.test import TestCase
from app.models import Asignatura,Archivo,Curso,Comentario,Notificacion,Valoracion,Usuario,Reporte,User
from app.forms import UsuarioForm,CursoForm,ReporteForm,UploadFileForm,CursoEditForm,ComentarioForm,ResponderComentarioForm,ResponderComentarioForm2,MonederoForm,ActualizarUsuarioForm
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now
import datetime
from datetime import timezone

# Estrategia: crear una clase por cada formulario
# Ejemplo: class AddCursoFormTest(TestCase):
# es importante que herede de TestCase
# Para saber más sobre la estrategia elegida visitar el siguiente link:
# https://adamj.eu/tech/2020/06/15/how-to-unit-test-a-django-form/
# Implementar como en la SECCION "Unit Tests" de dicho enlace


class addReportFormTests(TestCase):
    def test_report_form_is_valid(self):
        form_data = {
            'descripcion': 'Esto es una prueba',
            'tipo': 'PLAGIO'
        }
        form = ReporteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_report_form_description_empty(self):
        form_data = {
            'descripcion': None,
            'tipo': 'PLAGIO'
        }
        form = ReporteForm(data=form_data)
        self.assertTrue(form.has_error('descripcion'))
        self.assertTrue(
            '<ul class="errorlist"><li>descripcion<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))

    def test_report_form_tipo_empty(self):
        form_data = {
            'descripcion': 'Esto es una prueba',
            'tipo': None
        }
        form = ReporteForm(data=form_data)
        self.assertTrue(form.has_error('tipo'))
        self.assertTrue(
            '<ul class="errorlist"><li>tipo<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))

    def test_report_form_descripcion_too_large(self):
        form_data = {
            'descripcion': 'a'*501,
            'tipo': 'PLAGIO'
        }
        form = ReporteForm(data=form_data)
        self.assertTrue(form.has_error('descripcion'))
        self.assertTrue('<ul class="errorlist"><li>descripcion<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 500 caracteres (tiene 501).</li></ul></li></ul>' in str(form.errors))

    def test_report_form_descripcion_tipo(self):
        form_data = {
            'descripcion': 'Esto es una prueba',
            'tipo': 'MALO'
        }
        form = ReporteForm(data=form_data)
        self.assertTrue(form.has_error('tipo'))
        self.assertTrue(
            '<ul class="errorlist"><li>tipo<ul class="errorlist"><li>Escoja una opción válida. MALO no es una de las opciones disponibles.</li></ul></li></ul>' in str(form.errors))


class addUsuarioFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Asignatura.objects.create(
            nombre="Prueba", titulacion='Grado en Ingeniería Informática-Ingeniería del Software', anyo=2022)

    def test_user_form_is_valid(self):
        form_data = {
            'username': 'davbrican',
            'password': 'contrasenha',
            'confirm_password': 'contrasenha',
            'name': 'David',
            'surname': 'Brincau Cano',
            'email': 'david.brincau@htomail.com',
            'email_academico': 'davbrican@alum.us.es',
            'titulacion': 'Grado en Ingeniería Informática-Ingeniería del Software',
            'descripcion': 'Esto es una descripción de prueba',
            'terminos': True,
            'privacidad': True
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_all_empty(self):
        form_data = {
            'username': None,
            'password': None,
            'confirm_password': None,
            'name': None,
            'surname': None,
            'email': None,
            'email_academico': None,
            'titulacion': None,
            'descripcion': None,
            'terminos': True,
            'privacidad': True
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue('<ul class="errorlist"><li>username<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li><li>password<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li><li>confirm_password<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li><li>name<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li><li>surname<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li><li>email<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li><li>email_academico<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li><li>titulacion<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))

    def test_user_form_fields_too_large(self):
        form_data = {
            'username': 'a'*51,
            'password': 'a'*51,
            'confirm_password': 'a'*51,
            'name': 'a'*41,
            'surname': 'a'*41,
            'email': 'a'*254,
            'email_academico': 'a'*254,
            'titulacion': 'Grado en Ingeniería Informática-Ingeniería del Software',
            'descripcion': 'a'*501,
            'terminos': True,
            'privacidad': True
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue('<ul class="errorlist"><li>username<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 50 caracteres (tiene 51).</li></ul></li><li>password<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 50 caracteres (tiene 51).</li></ul></li><li>confirm_password<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 50 caracteres (tiene 51).</li></ul></li><li>name<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 40 caracteres (tiene 41).</li></ul></li><li>surname<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 40 caracteres (tiene 41).</li></ul></li><li>email<ul class="errorlist"><li>Introduzca una dirección de correo electrónico válida.</li></ul></li><li>email_academico<ul class="errorlist"><li>Introduzca una dirección de correo electrónico válida.</li></ul></li><li>descripcion<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 500 caracteres (tiene 501).</li></ul></li></ul>' in str(form.errors))

    def test_user_form_titulacion_inexistente(self):

        form_data = {
            'username': 'davbrican',
            'password': 'contrasenha',
            'confirm_password': 'contrasenha',
            'name': 'David',
            'surname': 'Brincau Cano',
            'email': 'david.brincau@htomail.com',
            'email_academico': 'davbrican@alum.us.es',
            'titulacion': 'Grado inventado',
            'descripcion': 'Esto es una descripción de prueba',
            'terminos': True,
            'privacidad': True
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue('<ul class="errorlist"><li>titulacion<ul class="errorlist"><li>Escoja una opción válida. Grado inventado no es una de las opciones disponibles.</li></ul></li></ul>' in str(form.errors))


class addFileFormTest(TestCase):
    def test_file_form_is_valid(self):
        with open('app/tests/test_files/test.pdf', 'rb') as upload_file:
            form = UploadFileForm(
                data={},
                files={
                    'file': SimpleUploadedFile(upload_file.name, upload_file.read()),
                }
            )
            self.assertTrue(form.is_valid())

    def test_file_form_file_none(self):
        with open('app/tests/test_files/test.pdf', 'rb') as upload_file:
            form = UploadFileForm(
                data={},
                files={
                    'file': None,
                }
            )
            self.assertTrue(
                '<ul class="errorlist"><li>file<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))

    def test_file_form_file_bad_codification(self):
        with open('app/tests/test_files/test.pdf', 'rb') as upload_file:
            form = UploadFileForm(
                data={},
                files={
                    'file': upload_file,
                }
            )
            self.assertTrue(
                '<ul class="errorlist"><li>file<ul class="errorlist"><li>No se ha enviado ningún fichero. Compruebe el tipo de codificación en el formulario.</li></ul></li></ul>' in str(form.errors))

    def test_file_form_file_empty(self):
        with open('app/tests/test_files/test.txt', 'rb') as upload_file:
            form = UploadFileForm(
                data={},
                files={
                    'file': SimpleUploadedFile(upload_file.name, upload_file.read()),
                }
            )
            self.assertTrue(
                '<ul class="errorlist"><li>file<ul class="errorlist"><li>El fichero enviado está vacío.</li></ul></li></ul>' in str(form.errors))


class addCursoFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Asignatura.objects.create(
            nombre="Prueba", titulacion='Grado en Ingeniería Informática-Ingeniería del Software', anyo=2022)
        user = User.objects.create(
            username='davbrican', password='contrasenha')
        Usuario.objects.create(nombre='David', apellidos='Brincau', email='david.brincau@hotmail.com',
                               email_academico='davbrican@alum.us.es', titulacion='Grado en Ingeniería Informática-Ingeniería del Software', descripcion='Descripcion1',
                               foto=None, dinero=12.0, django_user=user)

    def test_curso_form_is_valid(self):
        form_data = {
            "nombre": "Curso de prueba",
            "descripcion": "Esto es una descripción de prueba",
            "asignatura": "1"
        }

        user_sent = User.objects.first()
        form = CursoForm(user_sent, form_data)
        self.assertTrue(form.is_valid())

    def test_curso_form_empty_fields(self):
        form_data = {
            "nombre": None,
            "descripcion": None,
            "asignatura": None
        }

        user_sent = User.objects.first()
        form = CursoForm(user_sent, form_data)
        self.assertTrue('<ul class="errorlist"><li>nombre<ul class="errorlist"><li>Este campo es obligatorio</li></ul></li><li>descripcion<ul class="errorlist"><li>Este campo es obligatorio</li></ul></li><li>asignatura<ul class="errorlist"><li>Este campo es obligatorio</li></ul></li></ul>' in str(form.errors))

    def test_curso_form_invalid_asignatura(self):
        form_data = {
            "nombre": "Curso de prueba",
            "descripcion": "Esto es una descripción de prueba",
            "asignatura": "Asignatura de prueba"
        }

        user_sent = User.objects.first()
        form = CursoForm(user_sent, form_data)
        self.assertTrue(
            '<ul class="errorlist"><li>asignatura<ul class="errorlist"><li>Selecciona una opción válida</li></ul></li></ul>' in str(form.errors))
class putCursoFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        asignatura = Asignatura.objects.create(nombre="Prueba", titulacion='Grado en Ingeniería Informática-Ingeniería del Software', anyo=2022)
        user = User.objects.create(username='davbrican', password='contrasenha')
        usuario = Usuario.objects.create(nombre='David', apellidos='Brincau', email='david.brincau@hotmail.com', 
                               email_academico='davbrican@alum.us.es', titulacion='Grado en Ingeniería Informática-Ingeniería del Software', descripcion='Descripcion1', 
                               foto=None, dinero=12.0, django_user=user)  
        Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc), asignatura=asignatura, propietario=usuario)
        
    def test_put_curso_form_is_valid(self):
        usuario = User.objects.first()
        asignatura = Asignatura.objects.first()
        id_asi = asignatura.id
        form_data = {
            "nombre": "Nuevo nombre",
            "descripcion": "Nueva Descripcion",
            "asignatura": id_asi
        }
        
        curso_sent = Curso.objects.first()
        form = CursoEditForm(usuario,form_data, instance=curso_sent)
        self.assertTrue(form.is_valid())
        
    def test_put_curso_form_empty_fields(self):
        usuario = User.objects.first()
        form_data = {
            "nombre": None,
            "descripcion": None,
            "asignatura": None
        }
        
        curso_sent = Curso.objects.first()
        form = CursoEditForm(usuario,form_data, instance=curso_sent)
        self.assertTrue('<ul class="errorlist"><li>nombre<ul class="errorlist"><li>Este campo es obligatorio</li></ul></li><li>descripcion<ul class="errorlist"><li>Este campo es obligatorio</li></ul></li><li>asignatura<ul class="errorlist"><li>Este campo es obligatorio</li></ul></li></ul>' in str(form.errors))
        
        
    def test_put_curso_form_maxlength_error(self):
        usuario = User.objects.first()
        asignatura = Asignatura.objects.first()
        id_asi = asignatura.id
        form_data = {
            "nombre": "a"*101,
            "descripcion": "a"*501,
            "asignatura": id_asi
        }
        
        curso_sent = Curso.objects.first()
        form = CursoEditForm(usuario,form_data, instance=curso_sent)
        self.assertTrue('<ul class="errorlist"><li>nombre<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 100 caracteres (tiene 101).</li></ul></li><li>descripcion<ul class="errorlist"><li>La descripción no puede superar los 500 caracteres</li></ul></li></ul>' in str(form.errors))

class addComentarioFormTests(TestCase):
    def test_comentario_form_is_valid(self):
        form_data = {
            'texto': 'Esto es una prueba'
        }
        form = ComentarioForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_comentario_form_texto_empty(self):
        form_data = {
            'descripcion': None
        }
        form = ComentarioForm(data=form_data)
        self.assertTrue(form.has_error('texto'))
        self.assertTrue('<ul class="errorlist"><li>texto<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))

    def test_comentario_texto_too_large(self):
        
        form_data = {
            'texto': 'a'*501
        }
        form = ComentarioForm(data=form_data)
        self.assertTrue(form.has_error('texto'))
        self.assertTrue('<ul class="errorlist"><li>texto<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 500 caracteres (tiene 501).</li></ul></li></ul>' in str(form.errors))
        
class addResponderComentarioFormTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='davbrican2', password='contrasenha2')
        usuario = Usuario.objects.create(nombre='David2', apellidos='Brincau2', email='david.brincau@hotmail.com', 
                               email_academico='davbrican@alum.us.es', titulacion='Grado en Ingeniería Informática-Ingeniería del Software', descripcion='Descripcion1', 
                               foto=None, dinero=12.0, django_user=user)  
        asignatura = Asignatura.objects.create(nombre="Prueba2", titulacion='Grado en Ingeniería Informática-Ingeniería del Software', anyo=2022)
        curso = Curso.objects.create(nombre="Curso2", descripcion="Descripcion2", asignatura=asignatura, propietario=usuario, fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc))
        archivo = Archivo.objects.create(nombre="Archivo2", curso=curso, ruta="/")
        Comentario.objects.create(texto="Prueba2", usuario=usuario, archivo=archivo)
        
    def test_responder_comentario_form_is_valid(self):
        form_data = {
            'texto': 'Esto es una prueba',
            'responde_a': 1
        }
        form = ResponderComentarioForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_responder_comentario_form_texto_empty(self):
        form_data = {
            'texto': None,
            'responde_a': 1
        }
        form = ResponderComentarioForm(data=form_data)
        self.assertTrue(form.has_error('texto'))
        self.assertTrue('<ul class="errorlist"><li>texto<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))

    def test_responder_comentario_form_responde_a_empty(self):
        form_data = {
            'texto': 'Prueba',
            'responde_a': None
        }
        form = ResponderComentarioForm(data=form_data)
        self.assertTrue(form.has_error('responde_a'))
        self.assertTrue('<ul class="errorlist"><li>responde_a<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))


    def test_responder_comentario_texto_too_large(self):
        form_data = {
            'texto': 'a'*501,
            'responde_a': 1
        }
        form = ResponderComentarioForm(data=form_data)
        self.assertTrue(form.has_error('texto'))
        self.assertTrue('<ul class="errorlist"><li>texto<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 500 caracteres (tiene 501).</li></ul></li></ul>' in str(form.errors))
        
class addResponderComentario2FormTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='davbrican2', password='contrasenha2')
        usuario = Usuario.objects.create(nombre='David2', apellidos='Brincau2', email='david.brincau@hotmail.com', 
                               email_academico='davbrican@alum.us.es', titulacion='Grado en Ingeniería Informática-Ingeniería del Software', descripcion='Descripcion1', 
                               foto=None, dinero=12.0, django_user=user)  
        asignatura = Asignatura.objects.create(nombre="Prueba2", titulacion='Grado en Ingeniería Informática-Ingeniería del Software', anyo=2022)
        curso = Curso.objects.create(nombre="Curso2", descripcion="Descripcion2", asignatura=asignatura, propietario=usuario, fecha_publicacion=datetime.datetime.now().replace(tzinfo=timezone.utc))
        archivo = Archivo.objects.create(nombre="Archivo2", curso=curso, ruta="/")
        Comentario.objects.create(texto="Prueba2", usuario=usuario, archivo=archivo)
        
    def test_responder_comentario2_form_is_valid(self):
        form_data = {
            'texto': 'Esto es una prueba',
            'responde_a': 1,
            'usuario_responde_a': 'davbrican2'
        }
        form = ResponderComentarioForm2(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_responder_comentario2_form_texto_empty(self):
        form_data = {
            'texto': None,
            'responde_a': 1,
            'usuario_responde_a': 'davbrican2'
        }
        form = ResponderComentarioForm2(data=form_data)
        self.assertTrue(form.has_error('texto'))
        self.assertTrue('<ul class="errorlist"><li>texto<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))

    def test_responder_comentario2_form_responde_a_empty(self):
        form_data = {
            'texto': 'Prueba',
            'responde_a': None,
            'usuario_responde_a': 'davbrican2'
        }
        form = ResponderComentarioForm2(data=form_data)
        self.assertTrue(form.has_error('responde_a'))
        self.assertTrue('<ul class="errorlist"><li>responde_a<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))

    def test_responder_comentario2_form_usuario_responde_a_empty(self):
        form_data = {
            'texto': 'Prueba',
            'responde_a': 1,
            'usuario_responde_a': None
        }
        form = ResponderComentarioForm2(data=form_data)
        self.assertTrue(form.has_error('usuario_responde_a'))
        self.assertTrue('<ul class="errorlist"><li>usuario_responde_a<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))


    def test_responder_comentario2_texto_too_large(self):
        form_data = {
            'texto': 'a'*501,
            'responde_a': 1,
            'usuario_responde_a': 'davbrican2'
        }
        form = ResponderComentarioForm2(data=form_data)
        self.assertTrue(form.has_error('texto'))
        self.assertTrue('<ul class="errorlist"><li>texto<ul class="errorlist"><li>Asegúrese de que este valor tenga menos de 500 caracteres (tiene 501).</li></ul></li></ul>' in str(form.errors))
        
class addMonederoFormTests(TestCase):
    def test_monedero_form_is_valid(self):
        form_data = {
            'dinero': 15
        }
        form = MonederoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_monedero_form_dinero_empty(self):
        form_data = {
            'dinero': None
        }
        form = MonederoForm(data=form_data)
        self.assertTrue(form.has_error('dinero'))
        self.assertTrue('<ul class="errorlist"><li>dinero<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))

    def test_monedero_dinero_exceeds_min(self):
        
        form_data = {
            'dinero': 0.08
        }
        form = MonederoForm(data=form_data)
        self.assertTrue(form.has_error('dinero'))
        self.assertTrue('<ul class="errorlist"><li>dinero<ul class="errorlist"><li>Asegúrese de que este valor es mayor o igual a 0.09.</li></ul></li></ul>' in str(form.errors))
        
class updateUsuarioFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Asignatura.objects.create(nombre="Prueba", titulacion='Grado en Ingeniería Informática-Ingeniería del Software', anyo=2022)
    def test_update_usuario_form_is_valid(self):
        form_data = {
            'username': 'davbrican',
            'contrasena': 'contrasenha',
            'confirmar_contrasena': 'contrasenha',
            'nombre': 'David',
            'apellidos': 'Brincau',
            'email': 'davbrican@gmail.com',
            'titulacion': Asignatura.objects.first().titulacion,
            'descripcion': 'Descripcion',
            'foto': ''
        }
        form = ActualizarUsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_update_usuario_form_fields_empty(self):
        form_data = {
            'username': '',
            'contrasena': '',
            'confirmar_contrasena': '',
            'nombre': '',
            'apellidos': '',
            'email': '',
            'titulacion': Asignatura.objects.first().titulacion,
            'descripcion': '',
            'foto': ''
        }
        form = ActualizarUsuarioForm(data=form_data)
        self.assertTrue(form.has_error('username'))
        self.assertTrue(form.has_error('nombre'))
        self.assertTrue(form.has_error('apellidos'))
        self.assertTrue(form.has_error('email'))

    def test_update_usuario_too_much_characters_fields(self):
        form_data = {
            'username': 'a'*51,
            'contrasena': 'a'*51,
            'confirmar_contrasena': 'a'*51,
            'nombre': 'a'*41,
            'apellidos': 'a'*41,
            'email': 'a'*255,
            'titulacion': Asignatura.objects.first().titulacion,
            'descripcion': '',
            'foto': ''
        }
        form = ActualizarUsuarioForm(data=form_data)
        self.assertTrue(form.has_error('username'))
        self.assertTrue(form.has_error('contrasena'))
        self.assertTrue(form.has_error('confirmar_contrasena'))
        self.assertTrue(form.has_error('nombre'))
        self.assertTrue(form.has_error('apellidos'))
        self.assertTrue(form.has_error('email'))  
