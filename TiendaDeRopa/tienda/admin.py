from django.contrib import admin
from .models import(Cliente, Proveedor, Tipo, Color, Talla, Ropa, Inventario, Venta, DetalleVenta, PerfilUsuario)

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol')
    list_filter = ('rol',)


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'email', 'telefono')
    search_fields = ('nombre', 'apellidos', 'email')


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'email', 'telefono')
    search_fields = ('nombre_empresa', 'email')


class InventarioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'ropa', 'color', 'talla', 'unidades')
    list_filter = ('color', 'talla', 'ropa')
    search_fields = ('codigo', 'ropa__modelo')


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    readonly_fields = ('inventario', 'cantidad', 'precio_unitario')


class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'cliente', 'total')
    list_filter = ('fecha', 'cliente')
    search_fields = ('cliente__nombre', 'cliente__apellidos')
    readonly_fields = ('fecha', 'total')
    inlines = [DetalleVentaInline]


# Register your models here.
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Proveedor, ProveedorAdmin)

admin.site.register(Tipo)
admin.site.register(Color)
admin.site.register(Talla)
admin.site.register(Ropa)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta)