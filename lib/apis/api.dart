import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';

class Api extends GetConnect {
  var mostrar = false.obs;
  String gurl = 'http://localhost:5000';

  Future<Response> login(Map data) => post('$gurl/login', data);
}
