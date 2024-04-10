from django.db import models

# Create your models here.
class Producto(models.Model):
    codigo_barras = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre