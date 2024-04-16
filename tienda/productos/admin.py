from django.contrib import admin
from django.db.models import Sum
from .models import Producto, CarritoCompra, Venta

# Register your models here.
admin.site.register(Producto)
admin.site.register(CarritoCompra)
admin.site.register(Venta)
