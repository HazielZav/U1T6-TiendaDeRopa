from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.views import generic
from .models import Cliente, Color, Proveedor, Ropa, Inventario, Talla, Tipo, Venta, DetalleVenta
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import InventarioForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

#Clientes
class ClienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Cliente
    fields = ['nombre', 'apellidos', 'email', 'telefono']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_clientes')
    permission_required = 'tienda.add_cliente'

@login_required
@permission_required('tienda.view_cliente', raise_exception=True)
def lista_clientes(request):
    clientes = Cliente.objects.all()

    clientes = Cliente.objects.filter(activo=True)
    return render(request, "tienda/lista_clientes.html", {
        "clientes": clientes
    })

class ClienteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Cliente
    fields = ['nombre', 'apellidos', 'email', 'telefono']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_clientes')
    permission_required = 'tienda.change_cliente'

class ClienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Cliente
    success_url = reverse_lazy('lista_clientes')
    permission_required = 'tienda.delete_cliente'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # nomas por si acaso
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

# Inventario
@login_required
@permission_required('tienda.change_inventario', raise_exception=True)
def actualizar_inventario(request, pk):
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

#ROPa
class RopaCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Ropa
    fields = ['modelo', 'descripcion', 'marca', 'precio', 'tipo', 'proveedores']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('ropas')
    permission_required = 'tienda.add_ropa'

class RopaListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    #model = Ropa
    #queryset = Ropa.objects.filter(activo=True)
    context_object_name = 'ropa_list'
    template_name = 'tienda/ropa_list.html'
    permission_required = 'tienda.view_ropa'

    def get_queryset(self):
        # Esta línea hace el recuento total de todas las tallas/colores
        return Ropa.objects.filter(activo=True).annotate(total_inventario=Sum('inventario__unidades'))

class RopaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Ropa
    fields = ['modelo', 'descripcion', 'marca', 'precio', 'tipo', 'proveedores']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('ropas')
    permission_required = 'tienda.change_ropa'

class RopaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Ropa
    success_url = reverse_lazy('ropas')
    permission_required = 'tienda.delete_ropa'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # nomas por si acaso
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

# Color
class ColorListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Color
    template_name = 'tienda/color_list.html'
    context_object_name = 'colores'
    permission_required = 'tienda.view_color'
    queryset = Color.objects.filter(activo=True)

class ColorCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Color
    fields = ['nombre']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_colores')
    permission_required = 'tienda.add_color'

class ColorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Color
    fields = ['nombre']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_colores')
    permission_required = 'tienda.change_color'

class ColorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Color
    success_url = reverse_lazy('lista_colores')
    permission_required = 'tienda.delete_color'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # nomas por si acaso
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

#Tipo
class TipoListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Tipo
    template_name = 'tienda/tipo_list.html'
    context_object_name = 'tipos'
    permission_required = 'tienda.view_tipo'
    queryset = Tipo.objects.filter(activo=True)

class TipoCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Tipo
    fields = ['nombre']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_tipos')
    permission_required = 'tienda.add_tipo'

class TipoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Tipo
    fields = ['nombre']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_tipos')
    permission_required = 'tienda.change_tipo'

class TipoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Tipo
    success_url = reverse_lazy('lista_tipos')
    permission_required = 'tienda.delete_tipo'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # nomas por si acaso
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

# Talla
class TallaListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Talla
    template_name = 'tienda/talla_list.html'
    context_object_name = 'tallas'
    permission_required = 'tienda.view_talla'
    queryset = Talla.objects.filter(activo=True)

class TallaCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Talla
    fields = ['nombre']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_tallas')
    permission_required = 'tienda.add_talla'

class TallaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Talla
    fields = ['nombre']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_tallas')
    permission_required = 'tienda.change_talla'

class TallaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Talla
    success_url = reverse_lazy('lista_tallas')
    permission_required = 'tienda.delete_talla'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # nomas por si acaso
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

# PRoveedor
class ProveedorListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Proveedor
    template_name = 'tienda/proveedor_list.html'
    context_object_name = 'proveedores'
    permission_required = 'tienda.view_proveedor'
    queryset = Proveedor.objects.filter(activo=True)

class ProveedorCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Proveedor
    fields = ['nombre_empresa', 'email', 'telefono']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_proveedores')
    permission_required = 'tienda.add_proveedor'

class ProveedorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Proveedor
    fields = ['nombre_empresa', 'email', 'telefono']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_proveedores')
    permission_required = 'tienda.change_proveedor'

class ProveedorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Proveedor
    success_url = reverse_lazy('lista_proveedores')
    permission_required = 'tienda.delete_proveedor'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # nomas por si acaso
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

# Punto de venta
@login_required
@permission_required('tienda.add_venta', raise_exception=True)
def punto_de_venta(request):
    cliente_default, creado = Cliente.objects.get_or_create(
        nombre="Público general", 
        defaults = {
            "apellidos": "",
            "email": "",
            "telefono": ""
        }
    )
    clientes = Cliente.objects.all()

    inventario_disponible = Inventario.objects.filter(unidades__gt=0)

    venta = request.session.get('venta', {})

    items_venta = []
    total_venta = 0

    for inv_id, cantidad in venta.items():
        try:
            item = Inventario.objects.get(id=inv_id)
            subtotal = item.ropa.precio * cantidad
            total_venta += subtotal
            items_venta.append({
                'inventario': item,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except Inventario.DoesNotExist:
            continue

    return render(request, 'tienda/punto_de_venta.html', {
        'clientes': clientes,
        'cliente_default': cliente_default,
        'inventario': inventario_disponible,
        'items_venta': items_venta,
        'total_venta': total_venta
    })

@login_required
@permission_required('tienda.add_venta', raise_exception=True)
def agregar_a_venta(request, inv_id):
    if request.method == 'POST':
        cantidad_nueva = int(request.POST.get('cantidad', 1))
        inventario = get_object_or_404(Inventario, id=inv_id)

        venta = request.session.get('venta', {})

        cantidad_actual = venta.get(str(inv_id), 0)

        cantidad_total = cantidad_actual + cantidad_nueva

        if str(inv_id) in venta:
            messages.error(request, "Este artículo ya está en la lista. Ajusta la cantidad desde la lista de venta.")
        elif cantidad_total > inventario.unidades:
            messages.error(request, f"No hay suficientes unidades disponibles. Solo hay {inventario.unidades} en stock.")
        else:
            venta[str(inv_id)] = cantidad_total
            request.session['venta'] = venta
            messages.success(request, f"Se agregaron {cantidad_nueva} unidades de {inventario.ropa.modelo} a la venta.")

    return HttpResponseRedirect(reverse('punto_de_venta'))


def vaciar_venta(request):
    if 'venta' in request.session:
        del request.session['venta']
        messages.success(request, "Se limpió la venta.")
        
    return HttpResponseRedirect(reverse('punto_de_venta'))

def eliminar_de_venta(request, inv_id):
    venta = request.session.get('venta', {})
    
    # Si el artículo está en la venta
    if str(inv_id) in venta:
        del venta[str(inv_id)]
        request.session['venta'] = venta
        messages.success(request, "Artículo removido de la venta actual.")
        
    return HttpResponseRedirect(reverse('punto_de_venta'))

@login_required 
@transaction.atomic
def confirmar_venta(request):
    if request.method == 'POST':
        venta_session = request.session.get('venta', {})
        
        if not venta_session:
            messages.error(request, "El carrito está vacío.")
            return HttpResponseRedirect(reverse('punto_de_venta'))
        
        cliente_id = request.POST.get('cliente')
        if cliente_id:
            cliente = get_object_or_404(Cliente, id=cliente_id)
        else:
            cliente, _ = Cliente.objects.get_or_create(
                nombre='Público general', 
                defaults={'apellidos': ''}
            )

        nueva_venta = Venta.objects.create(
            cliente=cliente,
            cajero=request.user, # Asigna al usuario que inició sesión
            total=0
        )

        total_calculado = 0

        try:
            for inv_id, cantidad in venta_session.items():
                # select_for_update() bloquea la fila para evitar que otro cajero la venda al mismo tiempo
                inventario = Inventario.objects.select_for_update().get(id=inv_id)

                if inventario.unidades < cantidad:
                    raise Exception(f"Stock insuficiente de {inventario.ropa.modelo}")

                # Descontar de la BD
                inventario.unidades -= cantidad
                inventario.save()

                subtotal = inventario.ropa.precio * cantidad
                total_calculado += subtotal

                # Crear el renglón del ticket
                DetalleVenta.objects.create(
                    venta=nueva_venta,
                    inventario=inventario,
                    cantidad=cantidad,
                    precio_unitario=inventario.ropa.precio
                )

            nueva_venta.total = total_calculado
            nueva_venta.save()
            
            del request.session['venta']
            messages.success(request, f"Venta #{nueva_venta.id} procesada exitosamente.")
            
            return HttpResponseRedirect(reverse('ticket_venta', args=[nueva_venta.id]))

        except Exception as e:
            messages.error(request, str(e))
            return HttpResponseRedirect(reverse('punto_de_venta'))

    return HttpResponseRedirect(reverse('punto_de_venta'))

@login_required
def ticket_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'tienda/ticket_venta.html', {'venta': venta})