import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:websm/controllers/homectrl.dart';
import 'package:websm/screens/clientes.dart';

class Home extends StatefulWidget {
  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  @override
  Widget build(BuildContext context) {
    bool isHovered = false;
    bool isActive = false;

    final c = Get.put(Homectrl());

    return Scaffold(
      body: Obx(() {
        print(c.cambio.value);
        return Row(
          children: [
            Container(
              width: 200,
              height: double.infinity,
              decoration: buildBoxDecoration(),
              child: ListView(
                physics: ClampingScrollPhysics(),
                children: [
                  SizedBox(height: 50),
                  for (var i = 0; i < c.itemsmenu.length; i++)
                    itemenu(isHovered, isActive, '${c.itemsmenu[i]['nombre']}',
                        i, c, c.itemsmenu[i]['icono']),
                ],
              ),
            ),
            Expanded(
              child: Container(color: Colors.red, child: c.menuseleccionado),
            )
          ],
        );
      }),
    );
  }

  AnimatedContainer itemenu(bool isHovered, bool isActive, texto, i, c, icono) {
    return AnimatedContainer(
      duration: Duration(milliseconds: 250),
      color: isHovered
          ? Colors.white.withOpacity(0.1)
          : isActive
              ? Colors.white.withOpacity(0.1)
              : Colors.transparent,
      child: Material(
        color: Colors.transparent,
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 10, vertical: 10),
          child: MouseRegion(
            onEnter: (_) => setState(() => isHovered = true),
            onExit: (_) => setState(() => isHovered = false),
            child: Column(
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Icon(icono,
                        color: c.itemsmenu[i]['seleccionado']
                            ? Colors.amber
                            : Colors.white.withOpacity(0.3)),
                    SizedBox(width: 5),
                    GestureDetector(
                      onTap: () {
                        c.itemsmenu.forEach((v) {
                          if (v != c.itemsmenu[i]) v['seleccionado'] = false;
                        });
                        c.itemsmenu[i]['seleccionado'] =
                            !c.itemsmenu[i]['seleccionado'];
                        c.cambio.value = !c.cambio.value;
                      },
                      child: Text(
                        texto,
                        style: TextStyle(
                            fontSize: 16, color: Colors.white.withOpacity(0.8)),
                      ),
                    )
                  ],
                ),
                c.itemsmenu[i]['seleccionado']
                    ? Container(
                        padding: EdgeInsets.only(left: 5),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            for (var j = 0;
                                j < c.itemsmenu[i]['hijos'].length;
                                j++)
                              Container(
                                padding: EdgeInsets.symmetric(vertical: 10),
                                width: 130,
                                child: Row(
                                  children: [
                                    Icon(
                                      Icons.circle,
                                      size: 10,
                                      color: Colors.amber,
                                    ),
                                    SizedBox(
                                      width: 3,
                                    ),
                                    GestureDetector(
                                      onTap: () {
                                        //Get.to(Cliente());
                                        c.menuseleccionado = c.itemsmenu[i]
                                            ['hijos'][j]['pantalla'];
                                        c.cambio.value = !c.cambio.value;
                                      },
                                      child: Text(
                                        '${c.itemsmenu[i]['hijos'][j]['nombre']}',
                                        style: TextStyle(color: Colors.white),
                                      ),
                                    ),
                                  ],
                                ),
                              )
                          ],
                        ),
                      )
                    : SizedBox()
              ],
            ),
          ),
        ),
      ),
    );
  }

  BoxDecoration buildBoxDecoration() => BoxDecoration(
      gradient: LinearGradient(colors: [
        Color(0xff092044),
        Color(0xff092042),
      ]),
      boxShadow: [BoxShadow(color: Colors.black26, blurRadius: 10)]);
}
