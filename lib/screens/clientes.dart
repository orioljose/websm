import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../controllers/clientectrl.dart';

class Cliente extends StatelessWidget {
  const Cliente({super.key});

  @override
  Widget build(BuildContext context) {
    final c = Get.put(Clientectrl());
    return Container(
      child: Row(
        children: [
          Text('buscar'),
          Container(
            width: 100,
            height: 20,
            child: TextField(),
            decoration: BoxDecoration(
                border: Border.all(color: Colors.blue),
                borderRadius: BorderRadius.all(Radius.circular(5))),
          ),
          ElevatedButton(
              onPressed: () {
                c.pickFiles();
              },
              child: Text('Cargar'))
        ],
      ),
    );
  }
}
