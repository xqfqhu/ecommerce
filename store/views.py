from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import searchForm
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
    
        

    category_slug = request.GET.get('category')
    if "keyword" in request.GET:
        keyword = request.GET.get('keyword')
    else:
        keyword = ""


    if category_slug != "all":
        category = get_object_or_404(Category, slug = category_slug)
                
        category_recurse = category.recurse_children()
        products = Product.products.filter(
            category__in=category_recurse) & \
                (Product.products.filter(title__contains=keyword) | \
                    Product.products.filter(author__contains=keyword) | \
                        Product.products.filter(compiler__contains = keyword) | \
                            Product.products.filter(description__contains=keyword))

        response = render(request, 'store/category.html', {'products': products, 'category': category,  'keyword': keyword})
        return response
                
    else:
        products = Product.products.filter(title__contains=keyword) | \
                    Product.products.filter(author__contains=keyword) | \
                        Product.products.filter(compiler__contains = keyword) | \
                            Product.products.filter(description__contains=keyword)
        return render(request, 'store/category.html', {'products': products,  'keyword': keyword})
                
            
    
