from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('', views.all_products, name = 'store_home'),
    path('item/<slug:slug>/', views.product_detail, name = 'product_detail'),
    
    path("search", views.conduct_search, name="search"),
    
]