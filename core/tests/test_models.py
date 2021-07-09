
from django.test import TestCase
from store.models import Category, Product


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name = 'django', slug = 'django')
    def test_category_model_entry(self):
        '''
        the Category model data insertion attributes
        '''

        data = self.data1
        self.assertTrue(isinstance(data,Category))
    def test_category_model_entry(self):
        '''
        test Category model default name
        '''
        data = self.data1
        self.assertEqual(str(data), 'django')
