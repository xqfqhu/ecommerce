from django.db import models
from django.conf import settings
from django.urls import reverse

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', related_name = 'children', on_delete = models.CASCADE, blank = True, null = True)
    name = models.CharField(max_length = 225,db_index=True)
    slug = models.SlugField(max_length = 225, unique = True)
    introduction = models.CharField(max_length = 500, null = True, blank = True)
    # A "slug" is a way of generating a valid URL, generally using data already obtained.
    class Meta:
        verbose_name_plural = 'categories'
        # by default, django will have 'categorys' as the plural form
    def __str__(self):
        return self.name

    def _recurse_for_children(self, cat_obj):
        c_list = [cat_obj]
        children = cat_obj.children.all()
        if children.count() != 0:
            for child in children:
                more = self._recurse_for_children(child)
                c_list.extend(more)
        return c_list
    def recurse_children(self):
        instant_children = self.children.all()
        c_list = []
        for instant_child in instant_children:
            c_list.extend(self._recurse_for_children(instant_child))
        return {"instant_children": instant_children, "recurse_children": c_list}
            
class Product(models.Model):
    category = models.ForeignKey(Category, related_name = 'product', on_delete = models.CASCADE)
    # if you define a foreign field in a table, the table will have an entry called foreignField_id
    # you should use this foreignField_id rather than foriegnField to access this entry
    # see test_views.py for details
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'product_creator')
    title = models.CharField(max_length = 225)
    author = models.CharField(max_length = 225, blank = True)
    compiler = models.CharField(max_length = 225, blank = True)
    description = models.TextField(blank = True)
    # TextField allows more char than CharField
    image = models.ImageField(upload_to = 'images/')
    # it should be noted that we don't store images in the database. we store links to images in this database
    slug = models.SlugField(max_length = 225)
    price = models.DecimalField(max_digits = 4, decimal_places = 2)
    in_stock = models.BooleanField(default = True)
    is_active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    # triggered and recorded when added
    updated = models.DateTimeField(auto_now = True)
    # triggered and recorded when updated
    objects = models.Manager()
    products = ProductManager()
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created', )
        # -created means descending order in terms of created
        # created means ascending order in terms of created
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('store:product_detail', args = [self.slug])

