from django.contrib import admin
from .models import(Cliente, Proveedor, Tipo, Color, Talla, Ropa, Inventario, Venta, DetalleVenta, PerfilUsuario)

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Proveedor)

admin.site.register(Tipo)
admin.site.register(Color)
admin.site.register(Talla)
admin.site.register(Ropa)
admin.site.register(Inventario)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(PerfilUsuario)