from django.db import models

# Create your models here.


class Clientes(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Compras(models.Model):
    cliente_id = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    Tipos = [('contraentrega', 'Contraentrega'), ('en_oficina',
                                                  'En oficina'), ('en_direccion', 'En direccion'),]
    tipo = models.CharField(max_length=20, choices=Tipos)
    producto = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
