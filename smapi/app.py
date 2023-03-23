from flask import Flask, render_template, request, make_response, send_from_directory
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import json
import pymongo
from decimal import Decimal
import datetime
from multiprocessing import Process
from tinydb import TinyDB, Query

dbinicio = TinyDB('config.json')
# db.insert({
# 'type': 'config',
# 'host' : "localhost",
# 'puerto' : "5432",
# 'usuario' : "postgres",
# 'password' : "softmaster",
# 'db' : "cooperativa"
# })

Todo = Query()
config = dbinicio.search(Todo.type == 'config')


app = Flask(__name__)
CORS(app)


host = config[0]['host']
puerto = config[0]['puerto']
usuario = config[0]['usuario']
password = config[0]['password']
db = config[0]['db']
actividad = config[0]['actividad']

@app.route('/')
def index():
    return "apis soft master"

@app.route('/login', methods=['POST'])
def login():
    datos = request.json
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "select login, ssap from ssap where login='{}' and ssap='{}'".format(datos['usuario'], datos['password'])
    cursor.execute(sql)
    registros = cursor.fetchone()
    registros['actividad'] = actividad
    response = json.dumps(registros)
    return response

@app.route('/loginget/<u>/<p>', methods=['GET'])
def loginget(u,p):
    #datos = request.json
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "select login, ssap from ssap where login='{}' and ssap='{}'".format(u, p)
    cursor.execute(sql)
    registros = cursor.fetchone()
    registros['actividad'] = actividad
    response = json.dumps(registros)
    return response

@app.route('/config_activ', methods=['GET'])
def config_activ():
  config = dbinicio.search(Todo.type == 'config')
  resp = config[0]
  resp['msg'] = True
  response = json.dumps(resp)
  return response

@app.route('/ractividad', methods=['POST'])
def ractividad():
  datos = request.json
  dbinicio.upsert({
  'type': 'config',
  'host' : datos['txtservidor'],
  'puerto' : datos['txtpuerto'],
  'usuario' : datos['txtusuario'],
  'password' : datos['txtpassword'],
  'db' : datos['txtbasedatos'],
  'actividad': datos['txtactividad']
  }, Todo.type == 'config')
  db = datos['txtbasedatos']
  resp = {}
  resp['msg'] = True
  response = json.dumps(resp)
  return response
    

@app.route("/gen_xml")
def gen_xml():
  exe = "genera.exe"
  ctx = mp.get_context('spawn')
  q = ctx.Queue()
  p = ctx.Process(target=exe, args=(q,))
  p.start()



@app.route('/xml', methods=['POST'])
def xml():
  datos = request.json
  clavea = datos['claveacceso']
  correo = datos['çorreo']
  x4_tipo_amb = '1'
  x8_tipo_emis = '1'
  empresa = 'Fundación Jesús de la Misericordia'
  rucempresa = '1234568987654'
  telefempresa = '121212121'
  direcempresa = 'Av. Eloy Alfaro'
  tipocomprobante = '01'

  xmlstr = """"<?xml version="1.1" encoding="UTF-8" standalone="yes"?>
  <factura id="comprobante" version="1.1.0">
  <infoTributaria>
  <ambiente>{}</ambiente>
  <tipoEmision>{}</tipoEmision>
  <razonSocial>{}</razonSocial>
  <nombreComercial>{}</nombreComercial>
  <ruc>{}</ruc>
  <claveAcceso>{}</claveAcceso>
  <codDoc>{}</codDoc>
  <estab>{}</estab>
  <ptoEmi>{}</ptoEmi>
  <secuencial>{}</secuencial>
  <dirMatriz>{}</dirMatriz>
  </infoTributaria>
  """.format(x4_tipo_amb, x8_tipo_emis, empresa, empresa, rucempresa, clavea, tipocomprobante, serie_estab, serie_ptoemi, nexterno, direcempresa )
  return

# @app.route('validarcedula', methods = ['POST'])
# def validarcedula():
#   datos = request.json
#   numero = datos['numero']
#   tipo = datos['tipo']
#   if tipo == '1': #cédula
#     if len(numero) != 10:
#       msg = 'Número de dígitos inválido'
#   if tipo == '2':
#     if len(numero) != 13:
#       msg = 'Número de dígitos inválido'
      



@app.route('/newcli', methods=['POST'])
def newcli():
    datos = request.json
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "insert into climst (ruc_cedula, cliente, direc, telef1, e_mail) values('{}','{}','{}','{}','{}') returning cod_cli".format(datos['ruc_cedula'], datos['cliente'], datos['direc'], datos['telef1'], datos['e_mail'])
    cursor.execute(sql)
    conn.commit()
    resp = cursor.fetchone()
    response = json.dumps(resp)
    return response

@app.route('/getbodegas', methods=['GET'])
def getbodegas():
  connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
  conn = psycopg2.connect(connstr)
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
  sql = "select codigo, nombre1 from parmst where tipo_param=26 and codigo > 0"
  cursor.execute(sql)
  rbodegas = cursor.fetchall()
  respuesta = json.dumps(rbodegas, default=formato_respuesta)
  return respuesta



@app.route('/irfactura/<parametro>/<ntemporal>/<docum>')
def irfactura(parametro, ntemporal, docum):
  connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
  conn = psycopg2.connect(connstr)
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
  if parametro == 'primero':
    if docum == 'F':
      sql = "select min(numfac_cli) as posicion from clifac"
    else:
      sql = "select min(numfac_cli) as posicion from clitemp"
  elif parametro == 'anterior':
    ntemporal = int(ntemporal) - 1
    if docum == 'F':
      sql = "select numfac_cli as posicion from clifac where numfac_cli={}".format(ntemporal)
    else:
      sql = "select numfac_cli as posicion from clitemp where numfac_cli={}".format(ntemporal)
  elif parametro == 'posterior':
    ntemporal = int(ntemporal) + 1
    if docum == 'F':
      sql = "select numfac_cli as posicion from clifac where numfac_cli={}".format(ntemporal)
    else:
      sql = "select numfac_cli as posicion from clitemp where numfac_cli={}".format(ntemporal)
  elif parametro == 'ultimo':
    if docum == 'F':
      sql = "select max(numfac_cli) as posicion from clifac"
    else:
      sql = "select max(numfac_cli) as posicion from clitemp"
  cursor.execute(sql)
  regfactura = cursor.fetchone()
  respuesta = {}
  try:
    respuesta['posicion'] = regfactura['posicion']
  except:
    if parametro == 'anterior':
      respuesta['posicion'] = ntemporal - 1
    else:
      respuesta['posicion'] = ntemporal + 1
  resp = json.dumps(respuesta, default=formato_respuesta)
  return resp



@app.route('/consultarfactura/<numfac_cli>/<docum>')
def consultarfactura(numfac_cli, docum):
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    if docum == 'F':
      sql = "select a.numfac_cli, a.serie, a.n_externo, a.fecha, a.sri_clave_acc, b.ruc_cedula, b.cliente, b.direc, b.telef1, b.e_mail, a.suman, a.descuento, a.subtotal, a.subtot_iva, a.no_gravado, a.iva, a.totfin_fac, a.cod_cli from clifac as a, climst as b where a.cod_cli=b.cod_cli and a.numfac_cli={}".format(numfac_cli)
    else:
      sql = "select a.numfac_cli, a.serie, a.n_externo, a.fecha, a.sri_clave_acc, b.ruc_cedula, b.cliente, b.direc, b.telef1, b.e_mail, a.suman, a.descuento, a.subtotal, a.subtot_iva, a.no_gravado, a.iva, a.totfin_fac, a.cod_cli from clitemp as a, climst as b where a.cod_cli=b.cod_cli and a.numfac_cli={}".format(numfac_cli)
    cursor.execute(sql)
    regfactura = cursor.fetchone()
    if docum == 'F':
      sql = "select a.cod_secuen, b.cod_produc, a.cantidad, a.iva, a.p_venta, b.producto from  invtrn as a, invmst as b where a.tipo_doc_n=21 and a.n_comp={} and a.cod_secuen=b.cod_secuen".format(numfac_cli)
    else:
      sql = "select a.cod_secuen, b.cod_produc, a.cantidad, a.iva, a.p_venta, b.producto from  temptrn as a, invmst as b where a.tipo_doc_n=21 and a.n_comp={} and a.cod_secuen=b.cod_secuen".format(numfac_cli)

    cursor.execute(sql)
    regsproductos = cursor.fetchall()
    regsformaspago = []
    if docum == 'F':
      sql = "select a.numfac, a.tipo_doc_c, a.valor from clitrn as a where a.numfac = {}".format(numfac_cli)
      cursor.execute(sql)
      regsformaspago = cursor.fetchall()
    respuesta = {}
    regfactura['fecha'] = str(regfactura['fecha'])
    respuesta['factura'] = regfactura
    respuesta['productos'] = regsproductos
    respuesta['formaspago'] = regsformaspago
    resp = json.dumps(respuesta, default=formato_respuesta)
    return resp

@app.route('/getcliente/<ruc>', methods=['GET'])
def getcliente(ruc):
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "select cliente, direc,telef1,e_mail, cod_cli, tipo_ruc from climst where ruc_cedula='{}'".format(ruc)
    cursor.execute(sql)
    registros = cursor.fetchone()
    response = json.dumps(registros, default=formato_respuesta)
    return response

@app.route('/getclientenombre/<nombre>', methods=['GET'])
def getclientenombre(nombre):
    nombre = str(nombre).upper().replace(' ','%')
    
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "select cliente,ruc_cedula from climst where cliente like'%{}%'".format(nombre)
    cursor.execute(sql)
    registros = cursor.fetchall()
    response = json.dumps(registros)
    return response

def formato_respuesta(obj):
  if isinstance(obj, Decimal):
    return float(obj)



@app.route('/getproducto/<codigo>', methods=['GET'])
def getproducto(codigo):
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "select cod_produc, cod_secuen, producto, iva, p_venta from invmst where UPPER(cod_produc)=UPPER('{}') or UPPER(producto) like UPPER('%{}%')".format(codigo, codigo)
    cursor.execute(sql)
    campos = 'cod_produc,producto,p_venta,iva'
    camposarr = campos.split(',')
    registros = cursor.fetchall()
    response = json.dumps(registros, default=formato_respuesta)
    return response


@app.route('/getproductobodega/<codbodega>', methods=['GET'])
def getproductobodega(codbodega):
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "select cod_produc, cod_secuen, producto, iva, p_venta from invmst where cod_bodega={}".format(codbodega)
    cursor.execute(sql)
    campos = 'cod_produc,producto,p_venta,iva'
    camposarr = campos.split(',')
    registros = cursor.fetchall()
    response = json.dumps(registros, default=formato_respuesta)
    return response

@app.route('/getparametros', methods=['POST'])
def getparametros():
    parametros = request.json
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "select valor1, valor2, valor3, actuali, flag, solo_lis, status, sw_5, sw_6 from parmst where tipo_param={} and codigo={}".format(parametros['tipo_param'], parametros['codigo'])
    cursor.execute(sql)
    rparametros = cursor.fetchone()
    respuesta = json.dumps(rparametros, default=formato_respuesta)
    return respuesta


@app.route('/gettemporales')
def gettemporales():
  connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
  conn = psycopg2.connect(connstr)
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
  sql = "select fecha,numfac_cli,titular,totfin_fac,cajero from clifac where status=3 and anulado='false'"
  cursor.execute(sql)
  regs = cursor.fetchall()
  for r in regs:
    r['fecha'] = str(r['fecha'])

  respuesta = json.dumps(regs, default=formato_respuesta)
  return respuesta


# @app.route('/getproductos', methods=['GET'])
# def getproductos():
#     connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
#     conn = psycopg2.connect(connstr)
#     cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
#     sql = "select cod_produc, cod_secuen, producto, iva, p_venta from invmst "
#     cursor.execute(sql)
#     campos = 'cod_produc,producto,p_venta,iva'
#     camposarr = campos.split(',')
#     productos = cursor.fetchall()
#     response = json.dumps(productos, default=formato_respuesta)
#     return response


@app.route('/nuevo', methods = ['POST'])
def nuevo():
    datos = request.json
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    respuesta = {}
    respuesta['msg'] = False
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "insert into clifac (cajero,fecha) values('{}',now() ) RETURNING numfac_cli".format(datos['cod_user'])
    cursor.execute(sql)
    conn.commit()
    rnumfac_cli = cursor.fetchone()
    numfac_cli = rnumfac_cli['numfac_cli']
    return json.dumps(rnumfac_cli)


@app.route('/consultafp/<numfac_cli>', methods=['GET'])
def consultafp(numfac_cli):
  connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
  conn = psycopg2.connect(connstr)
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
  sql = "select tipo_doc_n as tipopago, fecha as fechafactura, cheque as numero, valor, fec_venci, numfac as numfac_cli, cod_cli from clitrn where numfac={}".format(numfac_cli)
  cursor.execute(sql)
  regs  =  cursor.fetchall()
  resp = {}
  resp['msg'] = 'ok'
  resparr = []
  for r in regs:
    r['fechafactura'] = str(r['fechafactura'])
    resparr.append(r)

  return json.dumps(resparr, default=formato_respuesta)

@app.route('/getnombrecuenta/<ncuenta>')
def getnombrecuenta(ncuenta):
  connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
  conn = psycopg2.connect(connstr)
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
  sql = """select b.cuenta,a.cliente,a.ruc_cedula, b.efectivo from climst a, ahmst b 
    where b.cuenta = a.cod_cli
    and a.cod_cli='{}'""".format(ncuenta)
  cursor.execute(sql)
  regs = cursor.fetchone()
  return json.dumps(regs, default=formato_respuesta)

@app.route('/trncajero')
def trncajero():
  connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
  conn = psycopg2.connect(connstr)
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
  sql = "select codigo,nombre1 from parmst where tipo_param=180 and codigo>0"
  cursor.execute(sql)
  regs = cursor.fetchall()
  return json.dumps(regs, default=formato_respuesta) 


@app.route('/postfp', methods=['POST'])
def postfp():
    fecha = datetime.datetime.now()
    r = request.json
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    try:
      sql = "delete from clitrn where numfac='{}'".format(r[0]['numfac_cli'])
      cursor.execute(sql)
      conn.commit()
    except:
      pass

    for fp in r:
        try:
          sql = "insert into clitrn(numfac,cod_cli, fecha, tipo_doc_n, valor, cheque) values('{}','{}','{}','{}','{}','{}')".format(fp['numfac_cli'],fp['cod_cli'],fp['fechafactura'], fp['tipopago'],fp['valor'],fp['numero'])
          cursor.execute(sql)
          conn.commit()
        except Exception as e:
          print(str(e))
    respuesta = {}
    respuesta['msg'] = True
    response = json.dumps(respuesta)
    return response



@app.route('/postinv', methods=['POST'])
def postinv():
    r = request.json
    numfac_cli = r['numfac_cli']
    decide = r['decide']
    serie = '001003'
    fecha = datetime.datetime.now()
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    respuesta = {}
    respuesta['msg'] = False
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    temporal = 0

    if decide == 0:
      n_externo = 0
    else:
      #temporal = numfac_cli
      #numfac_cli = 0
      sql = "select max(n_externo) as n_externo from clifac where serie='{}'".format(serie)
      cursor.execute(sql)
      n_externo = cursor.fetchone()
      if n_externo['n_externo'] == None:
        n_externo = 1
      else:
        n_externo = int(n_externo['n_externo']) + 1
      

      # for fp in r['formas_pago']:
      #   try:
      #     sql = "insert into clitrn(fecha, tipo, valor) values('{}','{}','{}')".format(fecha, fp['tipo'],fp['valor'])
      #     cursor.execute(sql)
      #     conn.commit()
      #   except Exception as e:
      #     print(str(e))


    error = True
    while error:
      try:
        nkard = int('21' + str(numfac_cli))
        #sql= "insert into clifac(numfac_cli, serie,ruc_cedula,fecha,totfin_fac) values('{}','{}','{}','{}','{}')".format(numfac_cli,serie,  r['ruc'], fecha, r['total'])
        if numfac_cli == 0:
          #if decide == 0:
          sql= """insert into clifac( serie,ruc_cedula,fecha,n_externo, nkard, suman, descuento, subtotal, subtot_iva, no_gravado, iva, totfin_fac, titular, cod_cli,status) 
          values('{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}',3) returning numfac_cli
          """.format(serie,  r['ruc'], fecha, n_externo, nkard, r['suman'], r['descuento'], r['subtotal'], r['tarifa_iva'], r['tarifa0'], r['iva'], r['total'], r['titular'], r['cod_cli'])
          #else:
          #  sql= """insert into clifac(temporal,serie,ruc_cedula,fecha,n_externo, nkard, suman, descuento, subtotal, subtot_iva, no_gravado, iva, totfin_fac, titular, cod_cli) 
          #  values('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}') returning numfac_cli
          #  """.format(temporal,serie,  r['ruc'], fecha, n_externo, nkard, r['suman'], r['descuento'], r['subtotal'], r['tarifa_iva'], r['tarifa0'], r['iva'], r['total'], r['titular'], r['cod_cli'])
          cursor.execute(sql)
          conn.commit()
          rnumfac_cli = cursor.fetchone()
          numfac_cli = rnumfac_cli['numfac_cli']
        else:
          sql= """update clifac set serie='{}',status=0,ruc_cedula='{}',fecha = '{}',n_externo='{}', nkard='{}', suman='{}', descuento='{}', subtotal='{}', subtot_iva='{}', no_gravado='{}', iva='{}', totfin_fac='{}', titular='{}', cod_cli='{}' where numfac_cli={} 
          """.format(serie,  r['ruc'], fecha, n_externo, nkard, r['suman'], r['descuento'], r['subtotal'], r['tarifa_iva'], r['tarifa0'], r['iva'], r['total'],r['titular'], r['cod_cli'], numfac_cli)
          cursor.execute(sql)
          conn.commit()
        error = False
      except Exception as e:
        print(str(e))
        pass

    error = True
    while error:
      try:
        #if decide == 1:
        sql= "update clifac set n_externo='{}' where numfac_cli='{}'".format(n_externo, numfac_cli)
        cursor.execute(sql)
        conn.commit()
        error = False
        
      except Exception as e:
        n_externo += 1
       

    #if decide == 1:
    sql = """ delete  from invtrn where n_comp={} and tipo_doc_n=21""".format(numfac_cli)
    cursor.execute(sql)
    conn.commit()
    for detalle in r['detalle']:
      sql = "insert into invtrn(n_comp, fecha, cantidad, cod_secuen, iva, p_venta, nkard, tipo_doc_n) values('{}','{}','{}','{}','{}','{}','{}','21')".format(numfac_cli ,fecha, detalle['cantidad'], detalle['cod_secuen'],detalle['iva'], detalle['p_venta'], nkard)
      cursor.execute(sql)
      conn.commit()
    # else:
    #   sql = """ delete  from temptrn where n_comp={}""".format(numfac_cli)
    #   cursor.execute(sql)
    #   conn.commit()
    #   for detalle in r['detalle']:
    #     sql = "insert into temptrn(n_comp, fecha, cantidad, cod_secuen, iva, p_venta, nkard, tipo_doc_n) values('{}','{}','{}','{}','{}','{}','{}','21')".format(numfac_cli ,fecha, detalle['cantidad'], detalle['cod_secuen'],detalle['iva'], detalle['p_venta'], nkard)
    #     cursor.execute(sql)
    #     conn.commit()
    
    respuesta['msg'] = True
    respuesta['numfac_cli'] = numfac_cli
    respuesta['n_externo'] = n_externo
    respuesta['serie'] = serie
    response = json.dumps(respuesta)
    return response

@app.route('/solicitar', methods=['POST'])
def solicitar():
  datos = request.json
  connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
  conn = psycopg2.connect(connstr)
  respuesta = {}
  respuesta['msg'] = False
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
  sql = """update clifac set estadosri = 'pendiente' where numfac_cli='{}'""".format(datos['numfac_cli'])
  cursor.execute(sql)
  conn.commit()
  cursor.close()
  conn.close()
  respuesta['msg'] = True
  response = json.dumps(respuesta)
  return response


@app.route('/grab_ah', methods=['POST'])
def grab_ah():
    r = request.json
    vcuenta = r['vcuenta']
    vtipo_doc_n = r['vtipo_doc_n']
    vvalor = r['vvalor']
    vfecha = datetime.datetime.now()

    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (host, puerto, usuario, password, db)
    conn = psycopg2.connect(connstr)
    respuesta = {}
    respuesta['msg'] = False
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    sql = """insert into ahtrn(fecha, cuenta, tipo_doc_n, valor, cod_age) 
    values('{}','{}','{}','{}',1)""".format(vfecha, vcuenta, vtipo_doc_n, vvalor)
    cursor.execute(sql)
    conn.commit()

    if vtipo_doc_n > 40:
      vvalor = '-' + vvalor
    else:
      vvalor = '+' + vvalor  

    sql = """update ahmst 
    set efectivo = efectivo {}
    where cuenta='{}' 
    """.format(vvalor,vcuenta)
    cursor.execute(sql)
    conn.commit()

    respuesta = {}
    respuesta['msg'] = True
    response = json.dumps(respuesta)
    return response

@app.route('/ver/<imagename>')
def images(imagename):
    return send_from_directory('Z:\\docum_el\\prefacturas', imagename)    

if __name__ == '__main__':
  app.run( port=5000, debug=True)
 
