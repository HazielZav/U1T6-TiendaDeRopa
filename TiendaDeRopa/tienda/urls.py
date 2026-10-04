from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('ropas/', views.RopaListView.as_view(), name='ropas'),
    path('ropa/<int:pk>/inventario/', views.actualizar_inventario, name='actualizar_inventario'),
    
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/<int:pk>/', views.detalle_venta, name='detalle_venta'),
]