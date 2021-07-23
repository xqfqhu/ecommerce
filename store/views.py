from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import searchForm
from django.http import HttpResponseRedirect
# Create your views here.


def all_products(request):
    products = Product.products.all()
    return render(request, 'store/index.html', {'products': products})


def categories(request):

    return {
        'categories':Category.objects.all()
    }

def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug, in_stock = True)

    return render(request, 'store/single.html', {'product': product})


def search(request):
    
    
        
    search_form = searchForm()
        
    return {'search_form':search_form}
def conduct_search(request):
    next_context = {}
    price_range_option = [0,5,10,25,50]
    num_range = len(price_range_option) 
    
    
    if "keyword" in request.GET:
        keyword = request.GET.get('keyword')
        if keyword != "":
            next_context['keyword'] = keyword
    else:
        keyword = ""
    products = Product.products.filter(title__contains=keyword) | \
        Product.products.filter(author__contains=keyword) | \
            Product.products.filter(compiler__contains = keyword) | \
                Product.products.filter(description__contains=keyword)


    category_slug = request.GET.get('category')
    if category_slug != "all":
        category = get_object_or_404(Category, slug = category_slug)
    
        category_recurse = category.recurse_children()
        products = Product.products.filter(category__in=category_recurse) & products
        next_context['category'] = category


    if "price-range" in request.GET:
        next_context['price-range'] = request.GET.get('price-range')
        price_range_idx = int(request.GET.get('price-range'))
        
        floor = price_range_option[price_range_idx-1]
        products = Product.products.filter(price__gte=floor) & products
        if price_range_idx < num_range:
            ceiling = price_range_option[price_range_idx]
            products = Product.products.filter(price__lte=ceiling) & products

    
    if len(next_context) == 0:
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        next_context['products'] = products
        return render(request, 'store/category.html',next_context)
        

    
            
        

    
    return response
                
            
    
