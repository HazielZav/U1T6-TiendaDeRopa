from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.views import generic
from .models import Cliente, Color, Proveedor, Ropa, Inventario, Talla, Tipo
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import InventarioForm

# Create your views here.

#Clientes
class ClienteCreateView(generic.CreateView):
    model = Cliente
    fields = ['nombre', 'apellidos', 'email', 'telefono']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('clientes')

def lista_clientes(request):
    clientes = Cliente.objects.all()

    return render(request, "tienda/lista_clientes.html", {
        "clientes": clientes
    })

# Inventario
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
class RopaCreateView(generic.CreateView):
    model = Ropa
    fields = ['modelo', 'descripcion', 'marca', 'precio', 'tipo', 'proveedores']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('ropas')

class RopaListView(generic.ListView):
    model = Ropa
    context_object_name = 'ropa_list'
    template_name = 'tienda/ropa_list.html'

    def get_queryset(self):
        # Esta línea hace el recuento total de todas las tallas/colores
        return Ropa.objects.annotate(total_inventario=Sum('inventario__unidades'))

# Color
class ColorListView(generic.ListView):
    model = Color
    template_name = 'tienda/color_list.html'
    context_object_name = 'colores'

class ColorCreateView(generic.CreateView):
    model = Color
    fields = ['nombre']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_colores')

#Tipo
class TipoListView(generic.ListView):
    model = Tipo
    template_name = 'tienda/tipo_list.html'
    context_object_name = 'tipos'

class TipoCreateView(generic.CreateView):
    model = Tipo
    fields = ['nombre']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_tipos')

# Talla
class TallaListView(generic.ListView):
    model = Talla
    template_name = 'tienda/talla_list.html'
    context_object_name = 'tallas'

class TallaCreateView(generic.CreateView):
    model = Talla
    fields = ['nombre']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_tallas')

# PRoveedor
class ProveedorListView(generic.ListView):
    model = Proveedor
    template_name = 'tienda/proveedor_list.html'
    context_object_name = 'proveedores'

class ProveedorCreateView(generic.CreateView):
    model = Proveedor
    fields = ['nombre_empresa', 'email', 'telefono']
    template_name = 'tienda/form_generico.html'
    success_url = reverse_lazy('lista_proveedores')