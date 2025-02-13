from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import include, path
from django.urls import path, include
from rest_framework import routers
from api.views import ComprasViewSet, ClientesViewSet


urlpatterns = [
    path("cliente/",
         ClientesViewSet.as_view({'get': 'list', 'post': 'create'}), name="Clientes"),





    path("compras/",
         ComprasViewSet.as_view({'post': 'crear_compra'}), name='Crear compra'),

    path("compras/<int:pk>", ComprasViewSet.as_view(
        {'get': 'obtener_compras_cliente'}), name="compras-cliente"),


    path('cliente/gasto_total/<int:pk>/', ClientesViewSet.as_view(
        {'get': 'obtener_gasto_total_cliente'}), name='gasto-total'),

    path('cliente/tipo/<int:pk>', ClientesViewSet.as_view(
        {'get': 'obtener_costo_por_tipo'}), name='costo por tipo')



] + debug_toolbar_urls()
