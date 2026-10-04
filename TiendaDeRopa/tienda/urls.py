from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('ropas/', views.RopaListView.as_view(), name='ropas'),
    path('ropa/<int:pk>/inventario/', views.actualizar_inventario, name='actualizar_inventario'),
]