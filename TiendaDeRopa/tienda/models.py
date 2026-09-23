from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    email = models.EmailField(max_length=80, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    email = models.EmailField(max_length=80, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre_empresa

class Tipo(models.Model):
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre

class Color(models.Model):
    nombre = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "Colores"

    def __str__(self):
        return self.nombre

class Talla(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Ropa(models.Model):
    modelo = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    marca = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.ForeignKey(Tipo, on_delete=models.RESTRICT)
    proveedores = models.ManyToManyField(Proveedor, related_name='ropas')

    def __str__(self):
        return f"{self.modelo} - {self.marca}"

class Inventario(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    unidades = models.PositiveIntegerField()
    ropa = models.ForeignKey(Ropa, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.RESTRICT)
    talla = models.ForeignKey(Talla, on_delete=models.RESTRICT)

    def __str__(self):
        return f"[{self.codigo}] {self.ropa.modelo} - {self.color.nombre} - {self.talla.nombre}"

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha.strftime('%Y-%m-%d')}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    inventario = models.ForeignKey(Inventario, on_delete=models.RESTRICT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)]) # Esto lo pusimos Carlos y yo porque no se puede vender 0 o menos unidades, es una validación muy sencilla para que no se pueda hacer eso 
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de Venta {self.venta.id} - {self.inventario.codigo}"