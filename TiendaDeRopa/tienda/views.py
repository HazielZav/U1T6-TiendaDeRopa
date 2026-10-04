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
    perfil = request.user.perfilusuario
    if perfil.rol not in ['ADMIN', 'ALMACENISTA']:
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