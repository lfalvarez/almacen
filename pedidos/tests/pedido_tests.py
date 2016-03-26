# coding=utf-8
from django.test import TestCase
from pedidos.models import Pedido, Categoria, Producto, Canasta, SeleccionProducto
from django.contrib.auth.models import User


class PedidoTestCase(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='feli',
                                                password='secreto',
                                                email='feli@almacencooperativo.cl')

    def test_create_one(self):
        pedido = Pedido.objects.create(nombre=u'Pedido del mes de Enero')
        self.assertTrue(pedido.slug)
        pedido2 = Pedido.objects.create(nombre=u'Pedido del mes de Enero')
        self.assertNotEquals(pedido.slug, pedido2.slug)

    def test_create_categoria_producto(self):
        categoria = Categoria.objects.create(nombre=u'Cereales, Semillas y Legumbres')
        self.assertTrue(categoria.slug)
        categoria2 = Categoria.objects.create(nombre=u'Cereales, Semillas y Legumbres')
        self.assertNotEquals(categoria.slug, categoria2.slug)

    def test_create_producto(self):
        categoria = Categoria.objects.create(nombre=u'Cereales, Semillas y Legumbres')
        producto = Producto.objects.create(nombre=u'Quinoa Orgánica a granel',
                                           precio=4800,
                                           descripcion=u'Producto Local, VI Región, Chile. Lavada (limpia).',
                                           categoria=categoria)
        self.assertTrue(producto.slug)

    def test_producto_en_pedido(self):
        categoria = Categoria.objects.create(nombre=u'Cereales, Semillas y Legumbres')
        producto = Producto.objects.create(nombre=u'Quinoa Orgánica a granel',
                                           precio=4800,
                                           descripcion=u'Producto Local, VI Región, Chile. Lavada (limpia).',
                                           categoria=categoria)
        pedido = Pedido.objects.create(nombre=u'Pedido del mes de Enero')
        pedido.productos.add(producto)
        self.assertTrue(pedido.productos.all())
        self.assertTrue(producto.pedidos.all())

    def test_pedido_de_usuario(self):
        pedido = Pedido.objects.create(nombre=u'Pedido del mes de Enero')
        pedido_de_usuario = Canasta.objects.create(usuario=self.usuario,
                                                   pedido=pedido)
        self.assertTrue(pedido_de_usuario.key)

    def test_canasta_con_productos(self):
        pedido = Pedido.objects.create(nombre=u'Pedido del mes de Enero')
        categoria = Categoria.objects.create(nombre=u'Cereales, Semillas y Legumbres')
        producto = Producto.objects.create(nombre=u'Quinoa Orgánica a granel',
                                           precio=4800,
                                           categoria=categoria,
                                           descripcion=u'Producto Local, VI Región, Chile. Lavada (limpia).')
        pedido.productos.add(producto)
        canasta = Canasta.objects.create(usuario=self.usuario,
                                         pedido=pedido)
        seleccion = SeleccionProducto.objects.create(producto=producto,
                                                     canasta=canasta,
                                                     cantidad=1)
        self.assertTrue(seleccion)

        canasta.agregar(producto, 2)
        seleccion_producto = canasta.productos.get(id=producto.id)
        self.assertEquals(seleccion_producto.cantidad, 3.0)
