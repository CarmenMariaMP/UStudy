from django.test import TestCase
from app.models import Asignatura,Archivo,Curso,Comentario,Notificacion,Valoracion,Usuario,Reporte
from app.forms import UsuarioForm,CursoForm,ReporteForm,UploadFileForm

## Estrategia: crear una clase por cada formulario
## Ejemplo: class AddCursoFormTest(TestCase):
## es importante que herede de TestCase
## Para saber más sobre la estrategia elegida visitar el siguiente link:
## https://adamj.eu/tech/2020/06/15/how-to-unit-test-a-django-form/
## Implementar como en la SECCION "Unit Tests" de dicho enlace

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
        self.assertTrue('<ul class="errorlist"><li>descripcion<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))
        
    def test_report_form_tipo_empty(self):
        form_data = {
            'descripcion': 'Esto es una prueba',
            'tipo': None
        }
        form = ReporteForm(data=form_data)
        self.assertTrue(form.has_error('tipo'))
        self.assertTrue('<ul class="errorlist"><li>tipo<ul class="errorlist"><li>Este campo es obligatorio.</li></ul></li></ul>' in str(form.errors))
        
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
        self.assertTrue('<ul class="errorlist"><li>tipo<ul class="errorlist"><li>Escoja una opción válida. MALO no es una de las opciones disponibles.</li></ul></li></ul>' in str(form.errors))


class addUsuarioFormTest(TestCase):
    def test_user_form_is_valid(self):
        form_data = {
            'username': '',
            'password': '',
            'confirm_password': '',
            'name': '',
            'surname': '',
            'email': '',
            'email_acade': '',
            'titulacion': '',
            'descripcion': ''
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())