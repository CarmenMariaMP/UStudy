import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from app.models import User, Usuario, Asignatura, Curso
import datetime
from datetime import timezone

## DEJAR DE UTILIZAR Y ELIMINAR ESTAS VARIABLES. EN SU LUGAR UTILIZAR self.live_server_url + PATH
BASEURL = 'http://localhost:8000/login/'
BASEURLSIGN = 'http://localhost:8000/registro/'
BASEURLCURSO = 'http://localhost:8000/crearcurso/'
BASEURLPROFILE = 'http://localhost:8000/perfil/'
BASEURLCOURSES = 'http://localhost:8000/cursosdisponibles'
#################################################################################################

# Test de login
class TestLogin(LiveServerTestCase):
    
    @classmethod
    def setUp(self): ## crear las entidades necesarias en este metodo para cada clase
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        option.add_argument("--headless") # evita mostrar el navegador
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
        user = User(username='prueba')
        user.set_password('contraseña')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com',
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        usuario.save()

    def test_login_erroneo(self):
        driver = self.driver
    
        driver.get(self.live_server_url+'/login/')

        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('prueba')
        contrasena.send_keys('contrasenha',Keys.ENTER)

        assert '/login' in driver.current_url

    def test_login_vacio(self):
        driver = self.driver
    
        driver.get(self.live_server_url+'/login/')

        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('')
        contrasena.send_keys('',Keys.ENTER)

        assert '/login' in driver.current_url


    def test_login_exitoso(self):
        driver = self.driver
    
        driver.get(self.live_server_url+'/login/')

        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('prueba')
        contrasena.send_keys('contraseña',Keys.ENTER)

        assert '/miscursos' in driver.current_url

# Test de registro

class TestRegistro(LiveServerTestCase):
    @classmethod
    def setUp(self): ## crear las entidades necesarias en este metodo para cada clase
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        option.add_argument("--headless") # evita mostrar el navegador
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
        user = User(username='prueba')
        user.set_password('contraseña')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com',
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        usuario.save()

    def test_registro_erroneo(self):
        driver = self.driver
    
        driver.get(self.live_server_url+'/registro/')

    

        
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
        driver = self.driver
    
        driver.get(self.live_server_url+'/registro/')
     
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
        driver = self.driver
        driver.get(self.live_server_url+'/registro/')
        driver.find_element(By.CSS_SELECTOR, "html").click()
        driver.find_element(By.ID, "id_username").send_keys("prueba22@@")
        driver.find_element(By.ID, "id_name").click()
        driver.find_element(By.ID, "id_name").send_keys("Prueba")
        driver.find_element(By.ID, "id_surname").send_keys("Prueba")
        driver.find_element(By.CSS_SELECTOR, "html").click()
        driver.find_element(By.ID, "id_password").send_keys("pacopaco")
        driver.find_element(By.ID, "id_confirm_password").click()
        driver.find_element(By.ID, "id_confirm_password").send_keys("pacopaco")
        driver.find_element(By.ID, "id_confirm_password").send_keys(Keys.ENTER)
        driver.find_element(By.ID, "siguiente").click()
        driver.find_element(By.ID, "id_email").click()
        driver.find_element(By.ID, "id_email").send_keys("pruebaprueba@hotmail.com")
        driver.find_element(By.ID, "id_email_academico").click()
        driver.find_element(By.ID, "id_email_academico").send_keys("pruebaprueba@alum.us.es")
        driver.find_element(By.ID, "siguiente2").click()
        driver.find_element(By.ID, "id_descripcion").click()
        driver.find_element(By.ID, "id_descripcion").send_keys("bnn")
        driver.find_element(By.ID, "id_terminos").click()
        driver.find_element(By.ID, "id_privacidad").click()
        driver.find_element(By.CSS_SELECTOR, ".row:nth-child(6) .btn:nth-child(2)").click()

        time.sleep(4)

        assert '/login' in driver.current_url

# Test de crear curso
class TestCrearCurso(LiveServerTestCase):

    @classmethod
    def setUp(self): ## crear las entidades necesarias en este metodo para cada clase
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        option.add_argument("--headless") # evita mostrar el navegador
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
        user = User(username='prueba')
        user.set_password('contraseña')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com',
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        usuario.save()
        asignatura = Asignatura.objects.create(
            nombre='Matemática Discreta', titulacion='Titulación 1', anyo=2012)
        asignatura.save()

    def test_crearcurso_fallido(self):
        driver = self.driver

        driver.get(self.live_server_url+'/login/')



        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('prueba')
        contrasena.send_keys('contraseña',Keys.ENTER)


        driver.get(self.live_server_url+'/crearcurso/')

        nombre = driver.find_element_by_name('nombre')
        descripcion = driver.find_element_by_name('descripcion')
        asignatura = driver.find_element_by_name('asignatura')

        nombre.send_keys('a')
        descripcion.send_keys('a')
        asignatura.send_keys('',Keys.ENTER)


        time.sleep(3)

        assert '/crearcurso' in driver.current_url

    def test_crearcuso_exitoso(self):
        driver = self.driver

        driver.get(self.live_server_url+'/login/')



        username = driver.find_element_by_name('username')
        contrasena = driver.find_element_by_name('contrasena')

        username.send_keys('prueba')
        contrasena.send_keys('contraseña',Keys.ENTER)

        driver.get(self.live_server_url+'/crearcurso/')

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
        
        time.sleep(1)

        aceptarSi=driver.find_element_by_id('aceptarSi')
        aceptarSi.click()

        time.sleep(3)

        assert '/inicio_profesor' in driver.current_url

## Test de editar perfil

class TestEditarPerfil(LiveServerTestCase):
    @classmethod
    def setUp(self): ## crear las entidades necesarias en este metodo para cada clase
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        option.add_argument("--headless") # evita mostrar el navegador
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
        user = User(username='prueba')
        user.set_password('contrasena')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com',
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        usuario.save()
        asignatura = Asignatura.objects.create(
            nombre='Nombre1', titulacion='Titulación 1', anyo=2012)
        asignatura.save()
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime.now(
        ).replace(tzinfo=timezone.utc), asignatura=asignatura, propietario=usuario)
        curso.save()

    def test_editarperfil_fallido(self):
        driver = self.driver
        driver.get(self.live_server_url+'/login/')
        driver.find_element(By.ID, "username").click()
        driver.find_element(By.ID, "username").send_keys("prueba")
        driver.find_element(By.ID, "pwd").send_keys("contrasena")
        driver.find_element(By.ID, "pwd").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, ".ml-auto > .nav-item:nth-child(2) > .nav-link").click()
        driver.find_element(By.ID, "editarPerfil").click()
        driver.find_element(By.ID, "id_contrasena").click()
        driver.find_element(By.ID, "id_contrasena").send_keys("pacopaco")
        driver.find_element(By.ID, "id_confirmar_contrasena").send_keys("pacopaco2")
        driver.find_element(By.ID, "actualizarBoton").click()

        time.sleep(3)

        assert '/actualizar_perfil' in driver.current_url
 
    def test_editarperfil_exitoso(self):
        driver = self.driver
        driver.get(self.live_server_url+'/login/')
        driver.find_element(By.ID, "username").click()
        driver.find_element(By.ID, "username").send_keys("prueba")
        driver.find_element(By.ID, "pwd").send_keys("contrasena")
        driver.find_element(By.ID, "pwd").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, ".bi-person-circle").click()
        driver.find_element(By.ID, "editarPerfil").click()
        driver.find_element(By.ID, "id_apellidos").click()
        element = driver.find_element(By.ID, "actualizarBoton")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        driver.find_element(By.ID, "id_apellidos").send_keys("alodate")
        driver.find_element(By.ID, "actualizarBoton").click()

        time.sleep(3)
        assert '/login' in driver.current_url

# Test de suscribirse a un curso

class TestEditarCurso(LiveServerTestCase):
    @classmethod
    def setUp(self): ## crear las entidades necesarias en este metodo para cada clase
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        option.add_argument("--headless") # evita mostrar el navegador
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
        user = User(username='prueba')
        user.set_password('contrasena')
        user.save()
        usuario = Usuario.objects.create(nombre='Nombre1', apellidos='Apellidos', email='email@hotmail.com',
                                         email_academico='barranco@alum.us.es', titulacion='Titulación 1',
                                         descripcion='Descripcion 1', foto='foto.jpg', dinero=9.53, django_user=user)
        usuario.save()
        asignatura = Asignatura.objects.create(
            nombre='Nombre1', titulacion='Titulación 1', anyo=2012)
        asignatura.save()
        curso = Curso.objects.create(nombre="Curso1", descripcion="Descripcion1", fecha_publicacion=datetime.datetime.now(
        ).replace(tzinfo=timezone.utc), asignatura=asignatura, propietario=usuario)
        curso.save()
        
    def test_editarcurso_exitoso(self):
        driver = self.driver
        driver.get(self.live_server_url+'/login/')
        driver.find_element(By.ID, "username").click()
        driver.find_element(By.ID, "username").send_keys("prueba")
        driver.find_element(By.CSS_SELECTOR, ".form-field:nth-child(3)").click()
        driver.find_element(By.ID, "pwd").click()
        driver.find_element(By.ID, "pwd").send_keys("contrasena")
        driver.find_element(By.ID, "pwd").send_keys(Keys.ENTER)
        element = driver.find_element(By.LINK_TEXT, "Alumno")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element = driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        driver.find_element(By.LINK_TEXT, "Profesor").click()
        driver.find_element(By.LINK_TEXT, "Gestionar Cursos").click()
        driver.find_element(By.LINK_TEXT, "Editar").click()
        driver.find_element(By.ID, "id_descripcion").send_keys("DescripcionX")
        driver.find_element(By.CSS_SELECTOR, ".btn").click()

        time.sleep(3)

        assert '/inicio_profesor' in driver.current_url

    def test_editarcurso_fallido(self):
        driver = self.driver
        driver.get(self.live_server_url+'/login/')
        driver.find_element(By.ID, "username").click()
        driver.find_element(By.ID, "username").send_keys("prueba")
        driver.find_element(By.CSS_SELECTOR, ".form-field:nth-child(3)").click()
        driver.find_element(By.ID, "pwd").click()
        driver.find_element(By.ID, "pwd").send_keys("contrasena")
        driver.find_element(By.ID, "pwd").send_keys(Keys.ENTER)
        element = driver.find_element(By.LINK_TEXT, "Alumno")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element = driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        driver.find_element(By.LINK_TEXT, "Profesor").click()
        driver.find_element(By.LINK_TEXT, "Gestionar Cursos").click()
        driver.find_element(By.LINK_TEXT, "Editar").click()
        driver.find_element(By.ID, "id_descripcion").click()
        element = driver.find_element(By.ID, "id_descripcion")
        actions = ActionChains(driver)
        actions.double_click(element).perform()
        driver.find_element(By.ID, "id_descripcion").send_keys(" ")
        driver.find_element(By.CSS_SELECTOR, ".btn").click()

        time.sleep(3)

        assert '/editarcurso' in driver.current_url
