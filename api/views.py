from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db.models import Sum  # Para la agregación de la suma
from .serializer import ClientesSerializer, ComprasSerializer, ClienteComprasSerializer
from .models import Clientes, Compras


class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer

    @action(detail=True, methods=['get'], url_path='gasto-total')
    def obtener_gasto_total_cliente(self, request, pk=None):
        """
        Obtiene el gasto total de un cliente.
        """
    # Obtiene el cliente o devuelve un error 404 si no existe
        cliente = get_object_or_404(Clientes, id=pk)

    # Suma el monto total de todas las compras del cliente
        gasto_total = Compras.objects.filter(cliente_id=cliente).aggregate(
            total_gasto=Sum('monto'))['total_gasto'] or 0

    # Devuelve el gasto total en un JSON
        return Response({'gasto_total': gasto_total})

    @action(detail=True, methods=['get'], url_path='costo-por-tipo')
    def obtener_costo_por_tipo(self, request, pk=None):
        """
        Devuelve el costo dependiendo del tipo de compra.
        """
        cliente = get_object_or_404(Clientes, id=pk)
        compras = Compras.objects.filter(cliente_id=cliente)
        resultado = []

        for compra in compras:
            if compra.tipo == 'contraentrega':
                costo = compra.monto - 400
            elif compra.tipo == 'en_oficina':
                costo = compra.monto  # Sin cambios en el costo
            elif compra.tipo == 'en_direccion':
                costo = compra.monto + 400
            else:
                costo = compra.monto  # Por si el tipo no es uno esperado
            resultado.append({'compra_id': compra.id, 'costo': costo})

        return Response(resultado)


class ComprasViewSet(viewsets.ModelViewSet):
    serializer_class = ComprasSerializer

    def get_queryset(self):
        """
        Filtra las compras por cliente_id si está en la URL.
        """
        cliente_id = self.kwargs.get('cliente_id')
        queryset = Compras.objects.all()
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        return queryset

    # Método para crear una compra
    @action(detail=False, methods=['post'], url_path='compras')
    def crear_compra(self, request):
        """
        Crea una nueva compra.
        Recibe el cliente_id, producto, tipo, monto y fecha.
        """
        # Se pasan los datos desde la solicitud
        serializer = self.ComprasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Guarda la compra en la base de datos
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ####################################################################################

    @action(detail=True, methods=['get'], url_path='compras-cliente')
    def obtener_compras_cliente(self, request, pk=None):

        cliente = get_object_or_404(Clientes, id=pk)
        # Usamos el serializador personalizado
        serializer = ClienteComprasSerializer(cliente)
        return Response(serializer.data)

    ####################################################################################

    ####################################################################################
