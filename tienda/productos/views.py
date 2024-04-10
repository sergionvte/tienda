from django.shortcuts import render, redirect
from .models import Producto
from django.http import JsonResponse
from django.forms.models import model_to_dict

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


def ventas(request):

    return render(request, 'ventas.html')




def informacion(request):
    return render(request, 'informacion.html')


def lista_compras(request):
    # Obtenemos la lista de compras de la sesión
    lista_compras = request.session.get('lista_compras', [])

    # Convertir cada producto en la lista de compras a un diccionario serializable
    serialized_productos = [model_to_dict(producto) for producto in lista_compras]

    # Pasar la lista de compras serializada al contexto del template
    return render(request, 'tu_template.html', {'lista_compras': serialized_productos})
