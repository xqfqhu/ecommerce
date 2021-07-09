from django.conf import settings
from importlib import import_module
from django.test import TestCase
from unittest import skip
from store.models import Category, Product
from django.test import Client # allow us to simulate a user
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from store.views import all_products

#@skip("demonstrating skipping") # allow you skip test and see that you're skipping one test
class TestViews(TestCase):
    def setUp(self):
        self.c = Client()
        User.objects.create(username = 'admin')
        Category.objects.create(name = 'django', slug = 'django')
        Product.objects.create(category_id = 1, title = 'django beginners',\
            created_by_id= 1, slug = 'django-beginners', price = 20, image = 'django')
    def test_url_allowed_hosts(self):
        '''
        test allowed hosts
        '''
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
    def test_product_detail_url(self):
        response = self.c.get(reverse("store:product_detail", args = ['django-beginners']))
        self.assertEqual(response.status_code,200)
    def test_category_list_url(self):
        
        response = self.c.get(reverse("store:category_list", args = ['django']))
        self.assertEqual(response.status_code,200)
    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title> Home </title>', html)