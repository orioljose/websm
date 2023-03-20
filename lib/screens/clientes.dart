import 'package:flutter/material.dart';

class Cliente extends StatelessWidget {
  const Cliente({super.key});

  @override
  Widget build(BuildContext context) {
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
          )
        ],
      ),
    );
  }
}
