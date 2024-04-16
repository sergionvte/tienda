from django.shortcuts import render, redirect
from .models import Producto, CarritoCompra, Venta
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.db.models import Sum
from django.utils import timezone

# Create your views here.
def index(request):
    productos = Producto.objects.all()

    # Calcular el total de ventas históricas
    total_ventas_historico = Venta.objects.aggregate(total=Sum('total'))['total'] or 0

    context = {
        'productos': productos,
        'total_ventas_historico': total_ventas_historico,
    }
    return render(
        request,
        'index.html',
        context,
    )


def registro(request):
    return render(request, 'registro.html')


def ventas(request):
    if request.method == 'POST':
        codigo_barras = request.POST.get('codigo_barras')
        try:
            producto = Producto.objects.get(codigo_barras=codigo_barras)
            if producto.cantidad_disponible > 0:
                # Verificar si hay suficiente stock para agregar al carrito
                carrito_item, created = CarritoCompra.objects.get_or_create(producto=producto)
                if not created and carrito_item.cantidad < producto.cantidad_disponible:
                    carrito_item.cantidad += 1
                    carrito_item.save()
                    messages.success(request, f"{producto.nombre} agregado al carrito.")
                else:
                    messages.error(request, f"No hay más stock disponible para {producto.nombre}.")
            else:
                messages.error(request, f"No hay disponibilidad para {producto.nombre}.")
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado.")

    productos = Producto.objects.all()
    carrito = CarritoCompra.objects.all()

    precio_total = sum(item.producto.precio * item.cantidad for item in carrito)

    context = {
        'productos': productos,
        'carrito': carrito,
        'precio_total': precio_total,
    }
    return render(request, 'ventas.html', context)


def pago(request):
    if request.method == 'POST':
        carrito = CarritoCompra.objects.all()

        # Calcular el total de la venta actual
        total_venta = sum(item.producto.precio * item.cantidad for item in carrito)

        # Procesar el pago y actualizar el stock
        for item in carrito:
            if item.producto.cantidad_disponible >= item.cantidad:
                item.producto.cantidad_disponible -= item.cantidad
                item.producto.save()
                item.delete()
            else:
                messages.error(request, f"No hay suficiente stock para {item.producto.nombre}.")

        # Crear una instancia de Venta y guardarla en la base de datos
        nueva_venta = Venta.objects.create(total=total_venta)
        nueva_venta.save()

        messages.success(request, "Pago procesado correctamente.")

        # Generar el contenido del ticket
        ticket_content = "Ticket de compra:\n\n"
        for item in carrito:
            ticket_content += f"Producto: {item.producto.nombre}\nCantidad: {item.cantidad}\nPrecio unitario: ${item.producto.precio}\n\n"
        ticket_content += f"Total de la compra: ${total_venta}\n"

        # Guardar el contenido del ticket en un archivo de texto
        filename = "ticket_venta.txt"
        with open(filename, 'w') as ticket_file:
            ticket_file.write(ticket_content)

        # Devolver el archivo de texto como una respuesta HTTP para que se descargue en el navegador
        with open(filename, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

    return redirect('ventas')



def eliminar_producto(request, codigo_barras):
    if request.method == 'POST':
        try:
            producto = Producto.objects.get(codigo_barras=codigo_barras)
            carrito_item = CarritoCompra.objects.get(producto=producto)
            if carrito_item.cantidad > 1:
                carrito_item.cantidad -= 1
                carrito_item.save()
            else:
                carrito_item.delete()
            messages.success(request, f"{producto.nombre} eliminado del carrito.")
        except (Producto.DoesNotExist, CarritoCompra.DoesNotExist):
            messages.error(request, "Producto no encontrado en el carrito.")

    return redirect('ventas')

