from django.shortcuts import render, get_object_or_404
from .basket import Basket
from store.models import Product
from django.http import JsonResponse


# Create your views here.

def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})
def basket(request):
    return {'basket': Basket(request)}
def basket_add(request):
    basket = Basket(request)
    
    if request.POST.get('action') == 'post':
        
        product_qty = int(request.POST.get('productqty'))

        product_id = str(request.POST.get('productid'))
        product = get_object_or_404(Product, id = int(product_id))
        basket.add(product = product, product_qty = product_qty)
        response = JsonResponse({'qty':basket.__len__()})
        
        return response
def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('productid'))
        
        product = get_object_or_404(Product, id = int(product_id))
        basket.delete(product = product)
        
        response = JsonResponse({'qty':str(basket.__len__()), 'subtotal': str(basket.get_total_price())})
        return response
def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_qty = int(request.POST.get('productqty'))
        product_id = str(request.POST.get('productid'))
        product = get_object_or_404(Product, id = product_id)
        basket.update(product = product, product_qty = product_qty)

        response = JsonResponse({'qty':str(basket.__len__()), 'subtotal': str(basket.get_total_price()), 'qtyThis': str(basket.basket[product_id]['qty'])})
        return response