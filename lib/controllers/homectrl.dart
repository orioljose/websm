import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:websm/screens/clientes.dart';
import 'package:websm/screens/inicio.dart';

class Homectrl extends GetxController {
  var cambio = false.obs;
  Widget menuseleccionado = Inicio();
  List itemsmenu = [
    {
      'nombre': 'Ventas',
      'seleccionado': false,
      'icono': Icons.menu,
      'hijos': [
        {'nombre': 'Clientes', 'seleccionado': false, 'pantalla': Cliente()},
        {'nombre': 'Facturación', 'seleccionado': false, 'pantalla': Inicio()},
        {
          'nombre': 'Nota de Credito',
          'seleccionado': false,
          'pantalla': Inicio()
        },
      ]
    },
    {
      'nombre': 'Compras',
      'seleccionado': false,
      'icono': Icons.shopping_basket,
      'hijos': [
        {'nombre': 'Proveedores', 'seleccionado': false},
        {'nombre': 'Ingreso de compra', 'seleccionado': false},
        {'nombre': 'Retenciones', 'seleccionado': false},
      ]
    },
    {
      'nombre': 'Inventarios',
      'icono': Icons.list,
      'seleccionado': false,
      'hijos': [
        {'nombre': 'Productos', 'seleccionado': false},
        {'nombre': 'Kardex', 'seleccionado': false},
      ]
    },
    {
      'nombre': 'Contabilidad',
      'icono': Icons.list,
      'seleccionado': false,
      'hijos': [
        {'nombre': 'Plan de cuentas', 'seleccionado': false},
        {'nombre': 'Comprobantes', 'seleccionado': false},
      ]
    },
    {
      'nombre': 'Administrador',
      'icono': Icons.list,
      'seleccionado': false,
      'hijos': [
        {'nombre': 'Usuarios', 'seleccionado': false},
        {'nombre': 'Parametros', 'seleccionado': false},
        {'nombre': 'Configuracion', 'seleccionado': false},
      ]
    },
    {
      'nombre': 'Salir',
      'icono': Icons.close,
      'seleccionado': false,
      'hijos': []
    },
  ];
}
