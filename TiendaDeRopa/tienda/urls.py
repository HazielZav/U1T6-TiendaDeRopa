from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='tienda/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='tienda/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

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

    path('punto-de-venta/', views.punto_de_venta, name='punto_de_venta'),
    path('punto-de-venta/agregar/<int:inv_id>/', views.agregar_a_venta, name='agregar_a_venta'),
    path('punto-de-venta/vaciar/', views.vaciar_venta, name='vaciar_venta'),
    path('punto-de-venta/eliminar/<int:inv_id>/', views.eliminar_de_venta, name='eliminar_de_venta'),
    path('punto-de-venta/confirmar/', views.confirmar_venta, name='confirmar_venta'),
    path('punto-de-venta/ticket/<int:venta_id>/', views.ticket_venta, name='ticket_venta'),

]