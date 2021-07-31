
from store.models import Product
from django.shortcuts import render, get_object_or_404

from payment.models import DeliveryOptions


class Basket():
    def __init__(self, request):

        self.session = request.session
        if 'basket' not in request.session:
            self.basket = self.session['basket'] = {}
        else:
            self.basket = self.session['basket']

    def add(self, product, product_qty):
        product_id = str(product.id)

        if product_id not in self.basket:
            self.basket[product_id] = {
                'price': str(
                    product.price),
                'qty': product_qty}
        else:
            self.basket[product_id]['qty'] += product_qty
        self.session.modified = True

    def delete(self, product):
        product_id = str(product.id)
        if product_id not in self.basket:
            return
        else:

            del self.basket[product_id]
            self.session.modified = True
            return

    def __len__(self):
        # you can call it with basket|length in html
        return sum(item['qty'] for item in self.basket.values())

    def get_subtotal_price(self):
        total = 0
        for item in self.basket.values():
            total += float(item['price']) * float(item['qty'])
        return round(total, 2)

    def get_delivery_price(self):
        subtotal = self.get_subtotal_price()
        delivery_price = 0
        if subtotal != 0 and 'purchase' in self.session:

            delivery_price = DeliveryOptions.objects.get(
                id=self.session['purchase']['delivery_id']).delivery_price
        return round(delivery_price, 2)

    def get_total_price(self):
        subtotal = self.get_subtotal_price()
        delivery_price = self.get_delivery_price()

        return round(float(subtotal) + float(delivery_price), 2)

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def update(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty

        self.session.modified = True

    def clear(self):

        del self.session['basket']
        if 'address' in self.session:
            del self.session['address']
        if 'purchase' in self.session:
            del self.session['purchase']
        self.session.modified = True
