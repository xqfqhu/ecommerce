from django.contrib import admin

# Register your models here.
from .models import DeliveryOptions, PaymentSelections


@admin.register(DeliveryOptions)
class DeliveryOptionsAdmin(admin.ModelAdmin):
    list_display = ['delivery_name', 'delivery_method', 'delivery_price',
                    'delivery_timeframe']


@admin.register(PaymentSelections)
class PaymentSelectionsAdmin(admin.ModelAdmin):
    list_display = ['name', ]
