from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_administracion, name='home_administracion'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_o_editar_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', views.crear_o_editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('empleados/crear/', views.crear_o_editar_empleado, name='crear_empleado'),
    path('empleados/editar/<int:id>/', views.crear_o_editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
    
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/crear/', views.crear_o_editar_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', views.crear_o_editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_o_editar_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.crear_o_editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('vehiculos/crear/', views.crear_o_editar_vehiculo, name='crear_vehiculo'),
    path('vehiculos/editar/<int:id>/', views.crear_o_editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),

    path('facturas/', views.lista_facturas, name='lista_facturas'),
    path('facturas/crear/', views.crear_o_editar_factura, name='crear_factura'),
    path('facturas/editar/<int:id>/', views.crear_o_editar_factura, name='editar_factura'),
    path('facturas/eliminar/<int:id>/', views.eliminar_factura, name='eliminar_factura'),

    


]
