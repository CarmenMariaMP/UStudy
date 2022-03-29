from django.test import TestCase
from app.models import Asignatura

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
    
    
          
            
        


