from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializer import ClientesSerializer, ComprasSerializer
from .models import Clientes, Compras

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer

class ComprasViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las Compras.
    """
    queryset = Compras.objects.all()
    serializer_class = ComprasSerializer

    @action(detail=False, methods=['post'])
    def crear_compra(self, request):
        """
        Crea una nueva Compra.
        """
        serializer = ComprasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='compras-cliente')
    def obtener_compras_cliente(self, request, pk=None):
        """
        Obtiene todas las compras de un cliente.
        """
        cliente = get_object_or_404(Clientes, id=pk)
        compras = Compras.objects.filter(cliente=cliente)
        serializer = ComprasSerializer(compras, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='gasto-total')
    def obtener_gasto_total_cliente(self, request, pk=None):
        """
        Obtiene el gasto total de un cliente.
        """
        cliente = get_object_or_404(Clientes, id=pk)
        compras = Compras.objects.filter(cliente=cliente)
        gasto_total = sum(compra.monto for compra in compras)
        return Response({'gasto_total': gasto_total})

    @action(detail=True, methods=['get'], url_path='costo-por-tipo')
    def obtener_costo_por_tipo(self, request, pk=None):
        """
        Obtiene el costo de cada compra de un cliente según su tipo.
        """
        cliente = get_object_or_404(Clientes, id=pk)
        compras = Compras.objects.filter(cliente=cliente)
        resultado = []

        for compra in compras:
            if compra.tipo == 'contraentrega':
                costo = compra.monto - 400
            elif compra.tipo == 'en_direccion':
                costo = compra.monto + 400
            else:
                costo = compra.monto
            resultado.append({'compra_id': compra.id, 'costo': costo})

        return Response(resultado)
