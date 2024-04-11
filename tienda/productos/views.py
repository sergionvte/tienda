from django.shortcuts import render, redirect
from .models import Producto
from django.contrib import messages
from django.http import JsonResponse
from django.forms.models import model_to_dict
from collections import Counter

# Create your views here.
def index(request):
    productos = Producto.objects.all()
    context = {
        'productos': productos,
    }
    return render(
        request,
        'index.html',
        context,
    )


def registro(request):
    return render(request, 'registro.html')


lista_compras = []

def ventas(request):
    global lista_compras

    if request.method == 'POST':
        codigo_barras = request.POST.get('codigo_barras')
        producto = Producto.objects.get(codigo_barras=codigo_barras)
        lista_compras.append(producto)

    # Calcular el conteo de cada producto en la lista de compras
    conteo_productos = dict(Counter(lista_compras))

    total_productos = sum([producto.precio for producto in lista_compras])
    context = {
        'lista_compras': lista_compras,
        'conteo_productos': conteo_productos,
        'total_productos': total_productos,
    }
    return render(request, 'ventas.html', context)


def eliminar_producto(request):
    if request.method == 'POST':
        codigo_barras = request.POST.get('codigo_barras')
        producto = Producto.objects.get(codigo_barras=codigo_barras)
        lista_compras.remove(producto)
    return redirect('ventas')


def informacion(request):
    return render(request, 'informacion.html')

