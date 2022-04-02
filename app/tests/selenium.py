import time
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
import requests


BASEURL = 'http://localhost:8000/login/'
BASEURLSIGN = 'http://localhost:8000/registro/'
BASEURLCURSO ='http://localhost:8000/crearcurso/'



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

class TestResgistro(LiveServerTestCase):
    def test_login_erroneo(self):
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

    def test_login_vacio(self):
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