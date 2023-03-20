import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:websm/screens/home.dart';

import '../apis/api.dart';

class Login extends StatelessWidget {
  const Login({super.key});

  @override
  Widget build(BuildContext context) {
    var size = MediaQuery.of(context).size;
    var usuario = TextEditingController(text: 'RR');
    var password = TextEditingController(text: '25570');
    return Scaffold(
      // appBar: AppBar(),
      body: Container(
        width: size.width,
        color: Colors.grey,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              'logo.bmp',
              width: 100,
            ),
            SizedBox(
              height: 10,
            ),
            Container(
              height: size.height * 0.3,
              width: 300,
              color: Colors.white,
              padding: EdgeInsets.symmetric(horizontal: 10),
              child: Column(
                children: [
                  Container(
                    child: TextField(
                      controller: usuario,
                      decoration: InputDecoration(label: Text('Usuario')),
                    ),
                  ),
                  Container(
                    child: TextField(
                      controller: password,
                      decoration: InputDecoration(label: Text('Clave')),
                    ),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  ElevatedButton(
                      onPressed: () async {
                        Map d = {};
                        d['usuario'] = usuario.text;
                        d['password'] = password.text;
                        try {
                          var r = await Api().login(d);
                          print(r.body);
                          if (r.body != null)
                            Get.to(Home());
                          else
                            Get.defaultDialog(
                                content: Text('Clave inválida',
                                    style: TextStyle(color: Colors.red)),
                                title: 'Mensaje de sistema');
                        } catch (e) {
                          Get.defaultDialog(
                              content: Text('Clave inválida',
                                  style: TextStyle(color: Colors.red)),
                              title: 'Mensaje de sistema');
                        }
                      },
                      child: Text('Ingresar'))
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
