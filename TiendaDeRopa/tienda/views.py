from django.shortcuts import render
from .models import Cliente

# Create your views here.
def lista_clientes(request):
    clientes = Cliente.objects.all()

    return render(request, "tienda/lista_clientes.html", {
        "clientes": clientes
    })