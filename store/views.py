from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import searchForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
# Create your views here.


def all_products(request):
    products = Product.products.all().prefetch_related("users_wishlist")
    return render(request, 'store/index.html', {'products': products})


def categories(request):

    return {
        'categories': Category.objects.all()
    }


def root_categories(request):

    return {
        'root_categories': Category.objects.filter(parent=None)
    }


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)

    return render(request, 'store/single.html', {'product': product})


def search(request):
    search_form = searchForm()
    return {'search_form': search_form}


def conduct_search(request):
    next_context = {}
    price_range_option = [0, 5, 10, 25, 50]
    num_range = len(price_range_option)

    if "keyword" in request.GET:
        keyword = request.GET.get('keyword')
        if keyword != "":
            next_context['keyword'] = keyword
    else:
        keyword = ""

    products = Product.products.filter(title__contains=keyword) | \
        Product.products.filter(author__contains=keyword) | \
        Product.products.filter(compiler__contains=keyword) | \
        Product.products.filter(description__contains=keyword)
    category_slug = request.GET.get('category')
    if category_slug != "all":
        category = get_object_or_404(Category, slug=category_slug)

        recurse_children = category.recurse_children()

        Category.objects.prefetch_related("children")
        instant_children = category.children.all()

        products = products.filter(category__in=recurse_children)
        next_context['category'] = category
        if len(instant_children) != 0:
            next_context['category_children'] = instant_children
    else:
        instant_children = Category.objects.all()
        if len(instant_children) != 0:
            next_context['category_children'] = instant_children

    if "price-range" in request.GET:
        next_context['price-range'] = request.GET.get('price-range')
        price_range_idx = int(request.GET.get('price-range'))

        floor = price_range_option[price_range_idx-1]
        products = products.filter(price__gte=floor) & products
        if price_range_idx < num_range:
            ceiling = price_range_option[price_range_idx]
            products = products.filter(price__lte=ceiling) & products

    if len(next_context) == 0:

        response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        next_context['products'] = products
        response = render(request, 'store/category.html', next_context)
    return response


@login_required
def edit_wishlist(request):
    if request.POST:
        referer = request.META["HTTP_REFERER"]
        redirect_flag = False
        if "item" in referer.split("/"):
            redirect_flag = True

        product_id = str(request.POST.get('productid'))
        product = get_object_or_404(Product, id=product_id)
        if product.users_wishlist.filter(id=request.user.id).exists():
            product.users_wishlist.remove(request.user)
            wishlist_action = "remove"
            if redirect_flag:
                messages.success(
                    request, "Removed {} to your Wish List".format(product.title))
        else:
            product.users_wishlist.add(request.user)
            wishlist_action = "add"
            if redirect_flag:
                messages.success(
                    request, "Added {} to your Wish List".format(product.title))
        if redirect_flag:
            response = HttpResponseRedirect(referer)
        else:
            response = JsonResponse({'wishlist_action': wishlist_action})
        return response
