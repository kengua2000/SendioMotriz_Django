from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_administracion, name='home_administracion'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_o_editar_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', views.crear_o_editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
]
