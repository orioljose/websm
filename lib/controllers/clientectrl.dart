import 'dart:convert';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:websm/screens/clientes.dart';
import 'package:websm/screens/inicio.dart';

import '../apis/api.dart';

class Clientectrl extends GetxController {
  var cambio = false.obs;
  Widget menuseleccionado = Inicio();
  var paths;
  var cargando = false.obs;

  void pickFiles() async {
    paths = (await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowMultiple: false,
      allowedExtensions: ['xlsx'],
    ))
        ?.files;
    print(paths[0].name);
    uploadFile(paths.first.bytes, paths.first.name);
    cargando.value = !cargando.value;
  }

  static Future<String> uploadFile(List<int> file, String fileName) async {
    FormData formData = FormData({});
    formData.files.add(MapEntry(
      "file",
      MultipartFile(file, filename: fileName),
    ));

    Map d = {};

    var respone = await Api().cargarfile(d);
    Map resp = jsonDecode(respone.body);

    Get.snackbar('Mensaje', 'Cargado con éxito', backgroundColor: Colors.white);
    return respone.body;
  }
}
