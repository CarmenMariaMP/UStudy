from django.test import TestCase
import pytest
import time
import json
import selenium
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC




# TESTS DE FRONTEND SPRINT 1

## Test de contraseña vacía y email correcto
class TestLogincontraseavacia(LiveServerTestCase):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    def setup_method(self, method):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome()
        self.vars = {}
  
    def teardown_method(self, method):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver.quit()
  
    def test_logincontraseavacia(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1552, 840)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "inputEmail").click()
        self.driver.find_element(By.ID, "inputEmail").send_keys("elenolcar@alum.us.es")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

## Test de email vacío y contraseña correcta
class TestLoginemailvacio(LiveServerTestCase):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    def setup_method(self, method):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome()
        self.vars = {}
  
    def teardown_method(self, method):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver.quit()
  
    def test_loginemailvacio(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1552, 840)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "show_hide_password").click()
        self.driver.find_element(By.ID, "show_hide_password").send_keys("contraseña")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

## Test de login exitoso

class TestLoginexitoso(LiveServerTestCase):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    def setup_method(self, method):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome()
        self.vars = {}
  
    def teardown_method(self, method):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver.quit()
  
    def test_loginexitoso(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1552, 840)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "inputEmail").click()
        self.driver.find_element(By.ID, "inputEmail").send_keys("elenolcar@alum.us.es")
        self.driver.find_element(By.ID, "show_hide_password").click()
        self.driver.find_element(By.ID, "show_hide_password").send_keys("contraseña")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
