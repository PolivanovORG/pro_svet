from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.apps import apps


class BasicTests(TestCase):
    
    def setUp(self):
        """Настройка тестового клиента"""
        self.client = Client()
    
    def test_home_page_status_code(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        # Ожидаем 200 OK или 302 redirect (если требует аутентификацию)
        self.assertIn(response.status_code, [200, 302])
    
    def test_admin_login_page_status_code(self):
        """Тест страницы входа в админку"""
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_settings_loaded_correctly(self):
        """Тест загрузки настроек"""
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertIn(type(settings.DEBUG), [bool])
        self.assertIsInstance(settings.ALLOWED_HOSTS, list)
    
    def test_basic_app_loaded(self):
        """Тест что основные приложения загружены"""
        self.assertIn('django.contrib.admin', settings.INSTALLED_APPS)
        self.assertIn('pro_svet', settings.INSTALLED_APPS)
    
    def test_pro_svet_app_config(self):
        """Тест конфигурации приложения pro_svet"""
        app_config = apps.get_app_config('pro_svet')
        self.assertEqual(app_config.name, 'pro_svet')
    
    def test_app_responds_to_requests(self):
        """Тест что приложение отвечает на HTTP-запросы"""
        response = self.client.get('/')
        # Проверяем, что ответ не None и имеет статус код
        self.assertIsNotNone(response)
        self.assertTrue(hasattr(response, 'status_code'))
        # Принимаем любые стандартные HTTP статусы
        self.assertIn(response.status_code, [200, 302, 403, 404])