from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class TestBasketView(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(
            category_id=1,
            created_by_id=1,
            title='django beginners',
            author='someone',
            image='django',
            slug='django-beginners',
            price='20.00')
        Product.objects.create(
            category_id=1,
            created_by_id=1,
            title='django intermediate',
            author='someone',
            image='django',
            slug='django-intermediate',
            price='20.00')
        Product.objects.create(
            category_id=1,
            created_by_id=1,
            title='django advanced',
            author='someone',
            image='django',
            slug='django-advanced',
            price='20.00')
        self.client.post(
            reverse('basket:basket_add'), {
                'productid': 1, 'productqty': 1, 'action': 'post'}, xhr=True)
        self.client.post(
            reverse('basket:basket_add'), {
                'productid': 1, 'productqty': 2, 'action': 'post'}, xhr=True)

    def test_basket_url(self):
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        response = self.client.post(
            reverse('basket:basket_add'), {
                'productid': 3, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('basket:basket_add'), {
                'productid': 3, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 5})
