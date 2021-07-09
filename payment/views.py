from decimal import *

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages


from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

from .models import DeliveryOptions
from basket.basket import Basket
from account.models import Address
from order.models import Order, OrderItem

CLIENT_ID = 'AVpfZG9llVun2lpUbvT3TkMArQGmiHqinQ_y9H-hsV56bpkJz6sv5Y0IbPpDxSurQsPC4rAcF6JUXQVE'
SECRET = 'EIpxt_LgP5Ofy93IYWJm_eNmag8ntV6LrGLayqDlnLjdvWf4FM1G6WbVgz6t831S8Trq5VBKAGIfwTI-'

@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active = True)
    basket = Basket(request)
    return render(request, 'payment/delivery_choices.html', {'deliveryoptions': deliveryoptions, 'basket': basket})

@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    subtotal = basket.get_subtotal_price()
    if request.POST.get('action') == 'post':
        deliveryid = int(request.POST.get('deliveryid'))
        delivery_option = get_object_or_404(DeliveryOptions, id = deliveryid)
        delivery_price = float(delivery_option.delivery_price)
        total = subtotal + delivery_price
        response = JsonResponse({'delivery_price':str(delivery_price), 'total': str(total)})
        
        session = request.session
        if 'purchase' not in request.session:
            session['purchase'] = {
                'delivery_id': deliveryid,
            }
        else:
            session['purchase']['delivery_id'] = deliveryid
        session_modified = True
        return response

@login_required
def delivery_address(request):
    session = request.session
    if 'purchase' not in session:
        messages.success(request, 'Please select delivery option')
        referer = request.META.get("HTTP_REFERER",'')
        if referer == '':
            referer = '/payment/deliverychoices'
        return HttpResponseRedirect(referer)
    else:
        
        addresses = Address.objects.filter(customer = request.user).order_by('-default') # .order_by('-default') asks django to put the "default" address at index 0
        if 'address' not in request.session:
            request.session['address'] = {'address_id': str(addresses[0].id)}
        else:
            request.session['address']['address_id'] = str(addresses[0].id)
        session.modified = True
        return render(request, 'payment/delivery_address.html', {'addresses': addresses})

@login_required
def payment_selection(request):
    if 'address' not in request.session:
        messages.success(request, 'Please select an address option.')
        referer = request.META.get("HTTP_REFERER",'')
        if referer == '':
            referer = '/payment/delivery_address'
        return HttpResponseRedirect(referer)
    return render(request, 'payment/payment_selection.html',{})

@login_required
def payment_complete(request):
    if request.method == 'POST':
        
        environment = SandboxEnvironment(client_id=CLIENT_ID, client_secret=SECRET)
        client = PayPalHttpClient(environment)
        
        orderID = request.POST.get('orderID')
        request_order = OrdersCaptureRequest(orderID)
        response = client.execute(request_order)
        
        basket = Basket(request)

        order = Order.objects.create(
            user = request.user,
            full_name=response.result.purchase_units[0].shipping.name.full_name,
            email=response.result.payer.email_address,
            address1=response.result.purchase_units[0].shipping.address.address_line_1,
            address2=response.result.purchase_units[0].shipping.address.admin_area_2,
            postal_code=response.result.purchase_units[0].shipping.address.postal_code,
            country_code=response.result.purchase_units[0].shipping.address.country_code,
            total_paid = Decimal(response.result.purchase_units[0].payments.captures[0].amount.value),
            order_key=response.result.id,
            payment_option="paypal",
            billing_status=True,
        )

        order_id = order.pk
        for item in basket:
            OrderItem.objects.create(
                order_id = order_id,
                product=item['product'],
                price = item['price'],
                quantity = item['qty']
            )
        return JsonResponse('Payment completed!', safe = False)
    else:
        messages.error(request, 'You have not paid yet!')
        referer = request.META.get("HTTP_REFERER",'')
        if referer == '':
            referer = '/payment/delivery_selection'
        return HttpResponseRedirect(referer)

@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    orderID = request.GET.get('order')

    order = get_object_or_404(Order, order_key=orderID)
    return render(request, 'payment/payment_successful.html', {'order':order})

