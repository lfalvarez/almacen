from __future__ import unicode_literals
from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth.models import User
import uuid


class Pedido(models.Model):
    nombre = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='nombre', unique=True)
    productos = models.ManyToManyField('Producto', related_name='pedidos')


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='nombre', unique=True)


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='nombre', unique=True)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria)


class Canasta(models.Model):
    usuario = models.ForeignKey(User, related_name='pedidos')
    pedido = models.ForeignKey(Pedido, related_name='usuarios')
    key = models.UUIDField(default=uuid.uuid4, editable=False)

    def agregar(self, producto, cantidad):
        seleccion_producto = self.productos.get(producto__id=producto.id)
        seleccion_producto.cantidad += cantidad
        seleccion_producto.save()


class SeleccionProducto(models.Model):
    producto = models.ForeignKey(Producto)
    canasta = models.ForeignKey(Canasta, related_name='productos')
    cantidad = models.FloatField()
