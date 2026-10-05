from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.views import generic
from .models import Cliente, Ropa, Inventario, Venta, DetalleVenta, PerfilUsuario
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import InventarioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction

# Create your views here.
@login_required
def inicio(request):
    return render(request, "tienda/inicio.html")

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()

    return render(request, "tienda/lista_clientes.html", {
        "clientes": clientes
    })

@login_required
def actualizar_inventario(request, pk):
    # Verificar que el usuario es ADMIN o ALMACENISTA
    try:
        perfil = request.user.perfilusuario
        rol = perfil.rol
    except:
        rol = 'ADMIN'

    if rol not in ['ADMIN', 'ALMACENISTA']:
        return render(request, 'tienda/error.html', {
            'mensaje': 'No tienes permiso para actualizar inventario.'
        })

    ropa = get_object_or_404(Ropa, pk=pk)
    inventarios = Inventario.objects.filter(ropa=ropa)
    
    # Lista para guardar parejas de (Objeto_Inventario, Su_Formulario)
    items_formulario = []

    if request.method == 'POST':
        todos_validos = True
        
        for inv in inventarios:
            # El "prefix" asegura que el input se llame "1-unidades", "2-unidades", etc.
            form = InventarioForm(request.POST, instance=inv, prefix=str(inv.id))
            items_formulario.append({'inventario': inv, 'form': form})
            
            if not form.is_valid():
                todos_validos = False
        
        if todos_validos:
            for item in items_formulario:
                item['form'].save() # Esto actualiza la base de datos limpiamente
            return HttpResponseRedirect(reverse('ropas'))

    else:
        for inv in inventarios:
            form = InventarioForm(instance=inv, prefix=str(inv.id))
            items_formulario.append({'inventario': inv, 'form': form})

    return render(request, 'tienda/actualizar_inventario.html', {
        'ropa': ropa,
        'items_formulario': items_formulario
    })

class RopaListView(generic.ListView):
    model = Ropa
    context_object_name = 'ropa_list'
    template_name = 'tienda/ropa_list.html'

    def get_queryset(self):
        # Esta línea hace el recuento total de todas las tallas/colores
        return Ropa.objects.annotate(total_inventario=Sum('inventario__unidades'))

@login_required
def crear_venta(request):
    # Verificar que el usuario es CAJERO o ADMIN
    try:
        perfil = request.user.perfilusuario
        rol = perfil.rol
    except:
        rol = 'ADMIN'

    if rol not in ['ADMIN', 'CAJERO']:
        return render(request, 'tienda/error.html', {
            'mensaje': 'No tienes permiso para realizar ventas.'
        })

    # Obtener o crear cliente "Público general"
    cliente_publico, _ = Cliente.objects.get_or_create(
        nombre='Público',
        apellidos='general'
    )

    clientes = Cliente.objects.all()
    inventarios = Inventario.objects.filter(unidades__gt=0).select_related('ropa', 'color', 'talla')

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        inventario_ids = request.POST.getlist('inventario')

        cliente = get_object_or_404(Cliente, pk=cliente_id)

        # Validar productos duplicados
        if len(inventario_ids) != len(set(inventario_ids)):
            return render(request, 'tienda/crear_venta.html', {
                'clientes': clientes,
                'inventarios': inventarios,
                'cliente_publico': cliente_publico,
                'error': 'No se permiten productos duplicados en la misma venta.'
            })

        # Validar cantidades y stock
        items_venta = []
        total = 0
        for inv_id in inventario_ids:
            cantidad = request.POST.get(f'cantidad_{inv_id}', '1')
            if not cantidad or int(cantidad) <= 0:
                continue

            inventario = get_object_or_404(Inventario, pk=inv_id)
            cantidad = int(cantidad)

            if cantidad > inventario.unidades:
                return render(request, 'tienda/crear_venta.html', {
                    'clientes': clientes,
                    'inventarios': inventarios,
                    'cliente_publico': cliente_publico,
                    'error': f'No hay suficiente stock para {inventario.ropa.modelo}. Disponible: {inventario.unidades}'
                })

            subtotal = cantidad * inventario.ropa.precio
            total += subtotal
            items_venta.append({
                'inventario': inventario,
                'cantidad': cantidad,
                'precio_unitario': inventario.ropa.precio,
                'subtotal': subtotal
            })

        if not items_venta:
            return render(request, 'tienda/crear_venta.html', {
                'clientes': clientes,
                'inventarios': inventarios,
                'cliente_publico': cliente_publico,
                'error': 'Debe seleccionar al menos un producto.'
            })

        # Crear venta y detalles
        with transaction.atomic():
            venta = Venta.objects.create(cliente=cliente, total=total)

            for item in items_venta:
                DetalleVenta.objects.create(
                    venta=venta,
                    inventario=item['inventario'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio_unitario']
                )
                # Descontar del inventario
                item['inventario'].unidades -= item['cantidad']
                item['inventario'].save()

        return HttpResponseRedirect(reverse('detalle_venta', kwargs={'pk': venta.id}))

    return render(request, 'tienda/crear_venta.html', {
        'clientes': clientes,
        'inventarios': inventarios,
        'cliente_publico': cliente_publico
    })

@login_required
def lista_ventas(request):
    # Verificar que el usuario es CAJERO o ADMIN
    try:
        perfil = request.user.perfilusuario
        rol = perfil.rol
    except:
        rol = 'ADMIN'

    if rol not in ['ADMIN', 'CAJERO']:
        return render(request, 'tienda/error.html', {
            'mensaje': 'No tienes permiso para consultar ventas.'
        })

    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'tienda/lista_ventas.html', {
        'ventas': ventas
    })

@login_required
def detalle_venta(request, pk):
    # Verificar que el usuario es CAJERO o ADMIN
    try:
        perfil = request.user.perfilusuario
        rol = perfil.rol
    except:
        rol = 'ADMIN'

    if rol not in ['ADMIN', 'CAJERO']:
        return render(request, 'tienda/error.html', {
            'mensaje': 'No tienes permiso para consultar ventas.'
        })

    venta = get_object_or_404(Venta, pk=pk)
    detalles = venta.detalles.all().select_related('inventario__ropa', 'inventario__color', 'inventario__talla')

    # Calcular subtotal para cada detalle
    for detalle in detalles:
        detalle.subtotal = detalle.precio_unitario * detalle.cantidad

    return render(request, 'tienda/detalle_venta.html', {
        'venta': venta,
        'detalles': detalles
    })