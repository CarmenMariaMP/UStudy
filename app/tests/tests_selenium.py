import time
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
import requests


BASEURL = 'http://localhost:8000/login/'
BASEURLSIGN = 'http://localhost:8000/registro/'
BASEURLCURSO = 'http://localhost:8000/crearcurso/'
BASEURLPROFILE = 'http://localhost:8000/perfil/'


## Test de login
class TestLogin(LiveServerTestCase):
    def test_login_erroneo(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
    
        driver.get(BASEURL)

    

        
        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('l@alum.us.es')
        contrasena.send_keys('prueba',Keys.ENTER)

        time.sleep(5)

        assert '/login' in driver.current_url


    def test_login_exitoso(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
    
        driver.get(BASEURL)

    

        
        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('prueba')
        contrasena.send_keys('contraseña',Keys.ENTER)

        time.sleep(3)

        assert '/miscursos' in driver.current_url

## Test de registro

class TestRegistro(LiveServerTestCase):
    def test_registro_erroneo(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
    
        driver.get(BASEURLSIGN)

    

        
        username = driver.find_element_by_name('username')
        name = driver.find_element_by_name('name')
        surname = driver.find_element_by_name('surname')
        password = driver.find_element_by_name('password')
        confirm_password = driver.find_element_by_name('confirm_password')

       

        username.send_keys('TestErroneo')
        name.send_keys('TestErroneo')
        surname.send_keys('TestErroneo')
        password.send_keys('TestErroneo')
        confirm_password.send_keys('TestErroneo',Keys.ENTER)

        time.sleep(5)

        assert '/registro' in driver.current_url

    def test_registro_vacio(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
    
        driver.get(BASEURLSIGN)
     
        username = driver.find_element_by_name('username')
        name = driver.find_element_by_name('name')
        surname = driver.find_element_by_name('surname')
        password = driver.find_element_by_name('password')
        confirm_password = driver.find_element_by_name('confirm_password')

    
        username.send_keys('')
        name.send_keys('')
        surname.send_keys('')
        password.send_keys('')
        confirm_password.send_keys('',Keys.ENTER)

        time.sleep(5)

        assert '/registro' in driver.current_url

    def test_registro_exitoso(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
    
        driver.get(BASEURLSIGN)

        username = driver.find_element_by_name('username')
        name = driver.find_element_by_name('name')
        surname = driver.find_element_by_name('surname')
        password = driver.find_element_by_name('password')
        confirm_password = driver.find_element_by_name('confirm_password')

        username.send_keys('pruebaUsuario')
        name.send_keys('prueba')
        surname.send_keys('prueba')
        password.send_keys('contraseña')
        confirm_password.send_keys('contraseña')

        time.sleep(2)

        siguiente=driver.find_element_by_id('siguiente')
        siguiente.click()


        email = driver.find_element_by_name('email')
        email_academico = driver.find_element_by_name('email_academico')

        email.send_keys('pruebaUsuario@gmail.com')
        email_academico.send_keys('pruebaUsuario@alum.us.es')

        time.sleep(2)

        siguiente2=driver.find_element_by_id('siguiente2')
        siguiente2.click()

        titulacion = driver.find_element_by_name('titulacion')
        descripcion = driver.find_element_by_name('descripcion')

        drop = Select(titulacion)
        drop.select_by_visible_text('Grado en Ingeniería Informática-Ingeniería del Software')
        descripcion.send_keys('esto es una descripción',Keys.ENTER)

        time.sleep(4)

        assert '/login' in driver.current_url

        
## Test de crear curso
class TestCrearCurso(LiveServerTestCase):
    def test_crearcuso_fallido(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)

        driver.get(BASEURL)



        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('prueba')
        contrasena.send_keys('contraseña',Keys.ENTER)


        driver.get(BASEURLCURSO)

        nombre = driver.find_element_by_name('nombre')
        descripcion = driver.find_element_by_name('descripcion')
        asignatura = driver.find_element_by_name('asignatura')

        nombre.send_keys('a')
        descripcion.send_keys('a')
        asignatura.send_keys('',Keys.ENTER)


        time.sleep(3)

        assert '/crearcurso' in driver.current_url

    def test_crearcuso_exitoso(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)

        driver.get(BASEURL)



        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('prueba')
        contrasena.send_keys('contraseña',Keys.ENTER)


        driver.get(BASEURLCURSO)

        nombre = driver.find_element_by_name('nombre')
        descripcion = driver.find_element_by_name('descripcion')
        asignatura = driver.find_element_by_name('asignatura')

        nombre.send_keys('Aprueba Matemáticas Discretas')
        descripcion.send_keys('Con este curso aprobarás seguro')

        drop = Select(asignatura)
        drop.select_by_visible_text('Matemática Discreta')

        time.sleep(2)

        crear=driver.find_element_by_id('crear')
        crear.click()

        time.sleep(3)

        assert '/inicio_profesor' in driver.current_url

## Test de editar perfil
class TestEditarPerfil(LiveServerTestCase):
    def test_editarperfil_fallido(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)

        driver.get(BASEURL)

        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('prueba')
        contrasena.send_keys('contraseña',Keys.ENTER)

        driver.get(BASEURLPROFILE)

        editarPerfil=driver.find_element_by_id('editarPerfil')
        editarPerfil.click()

        foto = driver.find_element_by_name('foto')
        username = driver.find_element_by_name('username')
        nombre = driver.find_element_by_name('nombre')
        apellidos = driver.find_element_by_name('apellidos')
        contrasena = driver.find_element_by_name('contrasena')
        confirmar_contrasena = driver.find_element_by_name('confirmar_contrasena')
        descripcion = driver.find_element_by_name('descripcion')
        email = driver.find_element_by_name('email')
        titulacion = driver.find_element_by_name('titulacion')

        username.clear()

        actualizarBoton=driver.find_element_by_id('actualizarBoton')
        actualizarBoton.click()

        time.sleep(3)

        assert '/actualizar_perfil' in driver.current_url
    
    def test_editarperfil_exitoso(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)

        driver.get(BASEURL)

        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('prueba')
        contrasena.send_keys('contraseña',Keys.ENTER)

        driver.get(BASEURLPROFILE)

        editarPerfil=driver.find_element_by_id('editarPerfil')
        editarPerfil.click()

        foto = driver.find_element_by_id('id_foto')
        username = driver.find_element_by_name('username')
        nombre = driver.find_element_by_name('nombre')
        apellidos = driver.find_element_by_name('apellidos')
        contrasena = driver.find_element_by_name('contrasena')
        confirmar_contrasena = driver.find_element_by_name('confirmar_contrasena')
        descripcion = driver.find_element_by_name('descripcion')
        email = driver.find_element_by_name('email')
        titulacion = driver.find_element_by_name('titulacion')

        foto.send_keys("\\app\\tests\\archivos_prueba\\foto_perfil.jpg")
        username.clear()
        username.send_keys('usuarioTest')
        nombre.clear()
        nombre.send_keys('Manolo')
        apellidos.clear()
        apellidos.send_keys('García')
        contrasena.clear()
        contrasena.send_keys('contrasena')
        confirmar_contrasena.send_keys('contrasena')
        descripcion.clear()
        descripcion.send_keys('Alumno dispuesto a enseñar con grandes calificaciones')
        email.clear()
        email.send_keys('manologarcia@gmail.com')

        actualizarBoton=driver.find_element_by_id('actualizarBoton')
        actualizarBoton.click()

        time.sleep(3)

        assert '/login' in driver.current_url
