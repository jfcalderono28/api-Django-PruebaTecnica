from rest_framework import serializers
from .models import Clientes, Compras


class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'


#*class ComprasSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Compras
#        fields = '__all__'
      
class ComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compras
        fields = ['id', 'cliente_id', 'tipo', 'producto', 'monto', 'fecha']

    def to_representation(self, instance):
        # Esto asegura que se muestre el ID en lugar del string de representación
        representation = super().to_representation(instance)
        representation['cliente_id'] = instance.cliente_id.id
        return representation # Campos específicos de la compra

class ClienteComprasSerializer(serializers.ModelSerializer):
    compras = ComprasSerializer(many=True, read_only=True)  # Relación con las compras

    class Meta:
        model = Clientes
        fields = ['nombre', 'email', 'compras']  # Campos del cliente + compras

