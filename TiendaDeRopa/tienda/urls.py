from django.urls import path, include
from . import views

urlpatterns = [
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='nuevo_cliente'),
    path('ropas/', views.RopaListView.as_view(), name='ropas'),
    path('ropa/nuevo/', views.RopaCreateView.as_view(), name='nueva_ropa'),
    path('ropa/<int:pk>/inventario/', views.actualizar_inventario, name='actualizar_inventario'),
    path('tipos/', views.TipoListView.as_view(), name='lista_tipos'),
    path('tipos/nuevo/', views.TipoCreateView.as_view(), name='nuevo_tipo'),
    path('tallas/', views.TallaListView.as_view(), name='lista_tallas'),
    path('tallas/nuevo/', views.TallaCreateView.as_view(), name='nueva_talla'),
    path('proveedores/', views.ProveedorListView.as_view(), name='lista_proveedores'),
    path('proveedores/nuevo/', views.ProveedorCreateView.as_view(), name='nuevo_proveedor'),
    path('colores/', views.ColorListView.as_view(), name='lista_colores'),
    path('colores/nuevo/', views.ColorCreateView.as_view(), name='nuevo_color'),
]