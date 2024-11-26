from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login2'),
    path('productos/', views.lista_productos2, name='lista_productos2'),
    path('vehiculos/', views.lista_vehiculos2, name='lista_vehiculos2'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('vehiculo/<int:id>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    path('logout/', views.logout, name='logout'),
    path('AcercadeNosotros/', views.acercadenosotros, name='acerca'),
]
