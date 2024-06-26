from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import os

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField(default=0)
    codigo_barras = models.CharField(max_length=50, primary_key=True)


    def clean(self):
        super().clean()
        if self.precio < 0:
            raise ValidationError("El precio no puede ser negativo.")
        if self.cantidad_disponible < 0:
            raise ValidationError("La cantidad disponible no puede ser negativa.")


    def __str__(self):
        return self.nombre


class CarritoCompra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


def get_upload_path(instance, filename):
    return os.path.join('tickets', 'venta_{instance.fecha.strftime("%d-%m-%Y")}.txt')


class Venta(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha_hora}"
