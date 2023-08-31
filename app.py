import os
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime, timedelta
from flask import send_from_directory
from tkinter import *
from tkinter import messagebox
from django import template
from django.db import models
from db import *
from usuarios import *
from logueo import *
from listar_cronograma import *
from calculo_vacaciones import *
from telefonos import *
from cumpleanos import *
import webbrowser
from creador_empresa import *
from creador_niveles import *

@app.route("/css/<archivocss>")
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/sitio/css'),archivocss)

@app.route('/')
def inicio():
    return render_template("/sitio/index.html")


@app.route('/admin_inicio')
def admin_inicio():

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from empresas")
    empresas=cursor.fetchall()
    conexion.commit
    cnt_empresas = int(empresas[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from gerencias")
    gerencias=cursor.fetchall()
    conexion.commit
    cnt_gerencias = int(gerencias[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from jefaturas")
    jefaturas=cursor.fetchall()
    conexion.commit
    cnt_jefaturas = int(jefaturas[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from niveles where id not in (99)")
    niveles=cursor.fetchall()
    conexion.commit
    cnt_niveles = int(niveles[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from reglas_vacaciones")
    reglas=cursor.fetchall()
    conexion.commit
    cnt_reglas = int(reglas[0][0])
    print (cnt_reglas)

    return render_template("admin/index.html", cnt_gerencias = cnt_gerencias, cnt_jefaturas = cnt_jefaturas, cnt_niveles = cnt_niveles, cnt_empresas = cnt_empresas, cnt_reglas = cnt_reglas)


@app.route('/inicio')
def inicio2():
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select * from noticias where apagar is null or apagar = 0")
    noticias=cursor.fetchall()
    conexion.commit
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from empleados where id_empleado = %s",(session["usuario"]))
    dato_usuario=cursor.fetchall()
    conexion.commit
    cnt_datos = int(dato_usuario[0][0])    
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from datos_contacto where id_empleado = %s",(session["usuario"]))
    dato_contacto=cursor.fetchall()
    conexion.commit
    cnt_contacto = int(dato_contacto[0][0])

    return render_template("sitio/inicio.html", noticias=noticias, cnt_datos = cnt_datos, cnt_contacto = cnt_contacto)


@app.route('/administrador')
def administrador():
    if not 'login' in session:
        return redirect("login")

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from empresas")
    empresas=cursor.fetchall()
    conexion.commit
    cnt_empresas = int(empresas[0][0])


    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from gerencias")
    gerencias=cursor.fetchall()
    conexion.commit
    cnt_gerencias = int(gerencias[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from jefaturas")
    jefaturas=cursor.fetchall()
    conexion.commit
    cnt_jefaturas = int(jefaturas[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from niveles where id not in (99)")
    niveles=cursor.fetchall()
    conexion.commit
    cnt_niveles = int(niveles[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from reglas_vacaciones")
    reglas=cursor.fetchall()
    conexion.commit
    cnt_reglas = int(reglas[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from usuario where funcion not in (99)")
    usuario=cursor.fetchall()
    conexion.commit
    cnt_usuario = int(usuario[0][0])



    return render_template("/admin/index.html", cnt_gerencias = cnt_gerencias, cnt_jefaturas = cnt_jefaturas, cnt_niveles = cnt_niveles, cnt_empresas = cnt_empresas, cnt_reglas = cnt_reglas, cnt_usuario = cnt_usuario)

@app.route('/img/<imagen>')
def imagenes(imagen):
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)

#######################################################
############ MANEJO DE LAS VACACIONES #################
#######################################################

@app.route('/vacaciones')
def vacaciones():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'pedidos_vacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _tiempocal = datetime.now()
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select case when dias_pendientes is null then 0 else dias_pendientes end from `stock_vacaciones` where id_empleado = %s;", (session["usuario"]))
    libros=cursor.fetchall()
    conexion.commit
    verificacion = int(libros[0][0])

    conexion=mysql.connect()
    sql = "Select id, empleado, date(desde), date(hasta), date(fecha_solicitud), estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador), fecha_aprobacion, case when estado in ('Aprobado','Rechazado') then 'hidden' else 'submit' end, case when estado in ('Aprobado','Rechazado') then '' else 'Eliminar' end, dias_totales, periodo from `vacaciones` where empleado = %s;"
    datos=(session["usuario"])
    stock = conexion.cursor()
    stock.execute(sql,datos)
    conexion.commit()
    return render_template("sitio/vacaciones.html", stock=stock, _tiempocal=_tiempocal, verificacion = verificacion)

@app.route('/stockvacaciones')
def stockvacaciones():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'stock_vacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT gerencia, jefatura, funcion, (select aprobacion from niveles where id = funcion),(select nivel from niveles where id = funcion) FROM `usuario` where nombre_usuario = %s", (session["usuario"]))
    condicionado=cursor.fetchall()
    conexion.commit
    gerencia = int(condicionado[0][0])
    jefatura = int(condicionado[0][1])
    funcion = int(condicionado[0][2])
    aprobacion = int(condicionado[0][3])
    seniority = str(condicionado[0][4])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id from niveles where nivel = 'Gerente'")
    es_gerente=cursor.fetchall()
    conexion.commit
    id_gerente = int(es_gerente[0][0])
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id from niveles where nivel = 'Jefe'")
    es_jefe=cursor.fetchall()
    conexion.commit
    id_jefe = int(es_jefe[0][0])
    

    if funcion == 99 or funcion == 108:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        sql = "SELECT `id`, (select concat(nombre, ' ', apellidos) from usuario where nombre_usuario = `id_empleado`), `periodo`, dias_totales, `dias_tomados`, `dias_pendientes`, `dias_por_aprobarse`, dias_aprobados FROM `stock_vacaciones` where (select activo from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo) > 0;"
        stock = conexion.cursor()
        stock.execute(sql)
        conexion.commit()
        return render_template("sitio/stockvacaciones.html", stock=stock)

    elif funcion == id_gerente:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("SELECT `id`, (select concat(nombre, ' ', apellidos) from usuario where nombre_usuario = `id_empleado`), `periodo`, dias_totales, `dias_tomados`, `dias_pendientes`, `dias_por_aprobarse`, dias_aprobados FROM `stock_vacaciones` where (select activo from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo) > 0 and id_empleado in (select nombre_usuario from usuario where gerencia = %s) ",(gerencia))     
        stock=cursor.fetchall()
        conexion.commit
    
        return render_template("sitio/stockvacaciones.html", stock=stock)

    elif funcion == id_jefe:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("SELECT `id`, (select concat(nombre, ' ', apellidos) from usuario where nombre_usuario = `id_empleado`), `periodo`, dias_totales, `dias_tomados`, `dias_pendientes`, `dias_por_aprobarse`, dias_aprobados FROM `stock_vacaciones` where (select activo from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo) > 0 and id_empleado in (select nombre_usuario from usuario where jefatura = %s)", (jefatura))
        stock=cursor.fetchall()
        conexion.commit
    
        return render_template("sitio/stockvacaciones.html", stock=stock)

    else:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("SELECT `id`, (select concat(nombre, ' ', apellidos) from usuario where nombre_usuario = `id_empleado`), `periodo`, dias_totales, `dias_tomados`, `dias_pendientes`, `dias_por_aprobarse`, dias_aprobados FROM `stock_vacaciones` where (select activo from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo) > 0  and id_empleado = %s", (session["usuario"]))
        stock=cursor.fetchall()
        conexion.commit
    
        return render_template("sitio/stockvacaciones.html", stock=stock)


@app.route('/vacaciones_acciones')
def vacaciones_acciones():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'vacaciones_acciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT gerencia, jefatura, funcion, (select aprobacion from niveles where id = funcion),(select nivel from niveles where id = funcion) FROM `usuario` where nombre_usuario = %s", (session["usuario"]))
    condicionado=cursor.fetchall()
    conexion.commit
    gerencia = int(condicionado[0][0])
    jefatura = int(condicionado[0][1])
    funcion = int(condicionado[0][2])
    aprobacion = int(condicionado[0][3])
    seniority = str(condicionado[0][4])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id from niveles where nivel = 'Gerente'")
    es_gerente=cursor.fetchall()
    conexion.commit
    id_gerente = int(es_gerente[0][0])
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id from niveles where nivel = 'Jefe'")
    es_jefe=cursor.fetchall()
    conexion.commit
    id_jefe = int(es_jefe[0][0])
    

    if funcion == 99 or funcion == 108:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select id, empleado, date_format(desde,'%d-%m-%Y'), date_format(hasta,'%d-%m-%Y'), date_format(desde,'%d-%m-%Y'), estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = empleado), dias_totales, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador) from `vacaciones` where estado = 'Pendiente de Aprobacion'")
        pendientes=cursor.fetchall()
        conexion.commit
    
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select id, empleado, date_format(desde,'%d-%m-%Y'), date_format(hasta,'%d-%m-%Y'), date_format(desde,'%d-%m-%Y'), estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = empleado), dias_totales, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador) from `vacaciones` where estado not in('Pendiente de Aprobacion')")
        no_pendientes=cursor.fetchall()
        conexion.commit
    

        return render_template("sitio/vacaciones_acciones.html", pendientes=pendientes, no_pendientes=no_pendientes)

    elif funcion == id_gerente:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select id, empleado, desde, hasta, fecha_solicitud, estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = empleado),dias_totales, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador) from `vacaciones` where estado = 'Pendiente de Aprobacion' and empleado in (select nombre_usuario from usuario where gerencia = %s) and empleado not in (%s)",(gerencia, session["usuario"]))     
        pendientes=cursor.fetchall()
        conexion.commit
    
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select id, empleado, desde, hasta, fecha_solicitud, estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = empleado), dias_totales, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador) from `vacaciones` where estado not in ('Pendiente de Aprobacion') and empleado in (select nombre_usuario from usuario where gerencia = %s) and empleado not in (%s)",(gerencia, session["usuario"]))     
        no_pendientes=cursor.fetchall()
        conexion.commit

        return render_template("sitio/vacaciones_acciones.html", pendientes=pendientes, no_pendientes = no_pendientes)
 
    elif funcion == id_jefe:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select id, empleado, desde, hasta, fecha_solicitud, estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = empleado), dias_totales, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador) from `vacaciones` where estado = 'Pendiente de Aprobacion' and empleado in (select nombre_usuario from usuario where jefatura = %s) and empleado not in (%s)", (jefatura, session["usuario"]))
        pendientes=cursor.fetchall()
        conexion.commit
    
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select id, empleado, desde, hasta, fecha_solicitud, estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = empleado), dias_totales, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador) from `vacaciones` where estado not in ('Pendiente de Aprobacion') and empleado in (select nombre_usuario from usuario where jefatura = %s) and empleado not in (%s)", (jefatura, session["usuario"]))
        no_pendientes=cursor.fetchall()
        conexion.commit

        return render_template("sitio/vacaciones_acciones.html", pendientes = pendientes, no_pendientes = no_pendientes)
 
    else:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select id, empleado, desde, hasta, fecha_solicitud, estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = empleado), dias_totales, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador) from `vacaciones` where estado in ('Pendiente de Aprobacion') and 1 = 2")
        pendientes=cursor.fetchall()
        conexion.commit
    
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select id, empleado, desde, hasta, fecha_solicitud, estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = empleado), dias_totales, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador) from `vacaciones` where estado not in ('Pendiente de Aprobacion') and 1 = 2")
        no_pendientes=cursor.fetchall()
        conexion.commit

        return render_template("sitio/vacaciones_acciones.html", pendientes = pendientes, no_pendientes = no_pendientes)
 

@app.route('/vacaciones/denegar', methods=['POST'])
def vacaciones_denegar():
 
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'vacaciones_denegar',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _id = request.form['txtId']
    _valor = request.form['Valor']
 
    sql = "update `vacaciones` set `estado` = %s, `aprobador` = %s, `fecha_aprobacion` = now() where id =%s;"
    datos=(_valor,session["usuario"],_id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    

    if _valor == "Aprobado":
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("SELECT periodo, dias_totales, empleado from vacaciones where id = %s",(_id))
        datos=cursor.fetchall()
        conexion.commit
        id_periodo = datos[0][0]
        id_diastotales = int(datos[0][1])
        id_empleado = datos[0][2]

        sql = "update stock_vacaciones set dias_aprobados = dias_aprobados + %s, dias_por_aprobarse = dias_por_aprobarse - %s where periodo = %s and id_empleado = %s;"
        datos= (id_diastotales, id_diastotales , id_periodo, id_empleado)
        conexion= mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()   

    elif _valor == "Rechazado":
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("SELECT periodo, dias_totales, empleado from vacaciones where id = %s",(_id))
        datos=cursor.fetchall()
        conexion.commit
        id_periodo = datos[0][0]
        id_diastotales = int(datos[0][1])
        id_empleado = datos[0][2]

        sql = "update stock_vacaciones set dias_pendientes = dias_pendientes + %s, dias_por_aprobarse = dias_por_aprobarse - %s where periodo = %s and id_empleado = %s;"
        datos= (id_diastotales, id_diastotales , id_periodo, id_empleado)
        conexion= mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()   

    return redirect("/vacaciones_acciones")


@app.route('/vacaciones/volver', methods=['POST'])
def vacaciones_volver():
 
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'vacaciones_volver',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _idvacaciones = request.form['Idvacaciones']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT periodo, dias_totales, empleado, estado from vacaciones where id = %s",(_idvacaciones))
    datos=cursor.fetchall()
    conexion.commit
    id_periodo = datos[0][0]
    id_diastotales = int(datos[0][1])
    id_empleado = datos[0][2]
    id_estado = datos[0][3]

    if id_estado == "Aprobado":

        sql = "update stock_vacaciones set dias_aprobados = dias_aprobados - %s, dias_por_aprobarse = dias_por_aprobarse + %s where periodo = %s and id_empleado = %s;"
        datos= (id_diastotales, id_diastotales , id_periodo, id_empleado)
        conexion= mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()   

        sql = "update `vacaciones` set `estado` = 'Pendiente de Aprobacion', `aprobador` = %s, `fecha_aprobacion` = now() where id =%s;"
        datos=(session["usuario"],_idvacaciones)
        conexion= mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(sql,datos)
        conexion.commit()

    elif id_estado == "Rechazado":

        sql = "update stock_vacaciones set dias_pendientes = dias_pendientes - %s, dias_por_aprobarse = dias_por_aprobarse + %s where periodo = %s and id_empleado = %s;"
        datos= (id_diastotales, id_diastotales , id_periodo, id_empleado)
        conexion= mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()   

        sql = "update `vacaciones` set `estado` = 'Pendiente de Aprobacion', `aprobador` = %s, `fecha_aprobacion` = now() where id =%s;"
        datos=(session["usuario"],_idvacaciones)
        conexion= mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(sql,datos)
        conexion.commit()


    return redirect("/vacaciones_acciones")


@app.route('/vacaciones/guardar', methods=['POST'])
def vacaciones_guardar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'vacaciones_guardar',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _tiempo = datetime.now()
    _desde = request.form['desde']
    _hasta = request.form['hasta']

    _aniodesde = _desde[0:4]
    _mesdesde = _desde[5:7]
    _diadesde = _desde[8:10]
    _desdenuevo = _aniodesde + '/' + _mesdesde + '/' + _diadesde
    _desdenuevofecha = datetime.strptime(_desdenuevo, '%Y/%m/%d')

    _aniohasta = _hasta[0:4]
    _meshasta = _hasta[5:7]
    _diahasta = _hasta[8:10]
    _hastanuevo = _aniohasta + '/' + _meshasta + '/' + _diahasta
    _hastanuevofecha = datetime.strptime(_hastanuevo, '%Y/%m/%d')
    _diasvacaciones = _hastanuevofecha + timedelta(days=1) - _desdenuevofecha

    _diasvacacionesentero = str(_diasvacaciones).replace(" days, 0:00:00","")
    _diasvacacionesentero = str(_diasvacacionesentero).replace(" day, 0:00:00","")
    _diasvacacionesentero

    if _desdenuevofecha > _hastanuevofecha:
    
        _tiempocal = datetime.now()

        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select case when sum(dias_pendientes) is null then 0 else sum(dias_pendientes) end from `stock_vacaciones` where id_empleado = %s;", (session["usuario"]))
        libros=cursor.fetchall()
        conexion.commit
        verificacion = int(libros[0][0])

        conexion=mysql.connect()
        sql = "Select id, empleado, date(desde), date(hasta), date(fecha_solicitud), estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador), fecha_aprobacion, case when estado in ('Aprobado','Rechazado') then 'hidden' else 'submit' end, case when estado in ('Aprobado','Rechazado') then '' else 'Eliminar' end, dias_totales, periodo from `vacaciones` where empleado = %s;"
        datos=(session["usuario"])
        stock = conexion.cursor()
        stock.execute(sql,datos)
        conexion.commit()
        
        return render_template("sitio/vacaciones.html", stock=stock, _tiempocal=_tiempocal, verificacion = verificacion, mensaje = "Los periodos seleccionados son incorrectos")
    else:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("SELECT sum(dias_pendientes) FROM `stock_vacaciones` WHERE (select activo from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo) > 0 and id_empleado = %s;", (session["usuario"]))
        vacas=cursor.fetchall()
        conexion.commit
        dias_totales = int(vacas[0][0])
        dias_solicitados = int(_diasvacacionesentero)

        periodo = 0
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("SELECT id, dias_pendientes, periodo FROM `stock_vacaciones` WHERE (select activo from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo) > 0 and id_empleado = %s order by periodo desc;",session["usuario"])
        vacas=cursor.fetchall()
        conexion.commit
        id_empleado = int(vacas[periodo][0])
        dias_por_periodo = int(vacas[periodo][1])
        nombre_periodo = vacas[periodo][2]

        print (dias_solicitados)
        print (dias_totales)

        if dias_solicitados <= dias_totales:
            while dias_solicitados > 0:
                if dias_solicitados <= int(vacas[periodo][1]):

                    sql = "update `stock_vacaciones` set `dias_por_aprobarse` = dias_por_aprobarse + %s, dias_pendientes = dias_pendientes - %s where id =%s;"
                    datos=(dias_solicitados, dias_solicitados, int(vacas[periodo][0]))
                    conexion= mysql.connect()
                    cursor = conexion.cursor()
                    cursor.execute(sql,datos)
                    conexion.commit()

                    sql = "INSERT INTO `vacaciones`(`empleado`, `desde`, `hasta`, `fecha_solicitud`, `estado`, `dias_totales`,periodo) VALUES (%s, %s, %s, %s, 'Pendiente de Aprobacion', %s, %s);"
                    datos=(session["usuario"], _desde,_hasta,_tiempo, dias_solicitados, vacas[periodo][2])
                    conexion= mysql.connect()
                    cursor = conexion.cursor()
                    cursor.execute(sql,datos)
                    conexion.commit()            

                    conexion=mysql.connect()
                    sql = "Select id, empleado, date(desde), date(hasta), date(fecha_solicitud), estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador), fecha_aprobacion, case when estado in ('Aprobado','Rechazado') then 'hidden' else 'submit' end, case when estado in ('Aprobado','Rechazado') then '' else 'Eliminar' end, dias_totales, periodo, case when estado in ('Aprobado','Rechazado') then 'Aprobado por: {{ stock[6] }} el dia: {{ stock[7] }}' else '' end from `vacaciones` where empleado = %s;"
                    datos=(session["usuario"])
                    stock = conexion.cursor()
                    stock.execute(sql,datos)
                    conexion.commit()
                    okvacas="Vacaciones cargadas correctamente"
                    return redirect("/vacaciones")
                else:
                    
                    sql = "update `stock_vacaciones` set `dias_por_aprobarse` = dias_por_aprobarse + `dias_pendientes`, dias_pendientes = 0 where id =%s;"
                    datos=(int(vacas[periodo][0]))
                    conexion= mysql.connect()
                    cursor = conexion.cursor()
                    cursor.execute(sql,datos)
                    conexion.commit()

                    sql = "INSERT INTO `vacaciones`(`empleado`, `desde`, `hasta`, `fecha_solicitud`, `estado`, `dias_totales`, periodo) VALUES (%s, %s, %s, %s, 'Pendiente de Aprobacion', %s, %s);"
                    datos=(session["usuario"], _desde,_hasta,_tiempo, int(vacas[periodo][1]), vacas[periodo][2])
                    conexion= mysql.connect()
                    cursor = conexion.cursor()
                    cursor.execute(sql,datos)
                    conexion.commit()            


                    dias_solicitados = dias_solicitados - dias_por_periodo
                    periodo = periodo + 1
        else:
            conexion=mysql.connect()
            sql = "Select id, empleado, date(desde), date(hasta), date(fecha_solicitud), estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador), fecha_aprobacion, case when estado in ('Aprobado','Rechazado') then 'hidden' else 'submit' end, case when estado in ('Aprobado','Rechazado') then '' else 'Eliminar' end, dias_totales, periodo from `vacaciones` where empleado = %s;"
            datos=(session["usuario"])
            stock = conexion.cursor()
            stock.execute(sql,datos)
            conexion.commit()
            
            _tiempocal = datetime.now()

            conexion=mysql.connect()
            cursor=conexion.cursor()
            cursor.execute("Select case when sum(dias_pendientes) is null then 0 else sum(dias_pendientes) end from `stock_vacaciones` where id_empleado = %s;", (session["usuario"]))
            libros=cursor.fetchall()
            conexion.commit
            verificacion = int(libros[0][0])

            
            return render_template("sitio/vacaciones.html", stock=stock, _tiempocal=_tiempocal, verificacion = verificacion, mensaje = "Exceso de stock de vacaciones, cuentas con " + str(dias_totales) + " dias de vacaciones.")



@app.route('/vacaciones/borrar', methods=['POST'])
def vacaciones_borrar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'vacaciones_borrar',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _id = request.form['txtId']
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM `vacaciones` WHERE id=%s", (_id))
    stock=cursor.fetchall()
    conexion.commit()
    
    _periodo = request.form['periodoId']
    _diassolicitados = request.form['diassolicitadosId']
    
    sql = "update `stock_vacaciones` set dias_por_aprobarse = dias_por_aprobarse - %s, dias_pendientes = dias_pendientes + %s WHERE periodo=%s and id_empleado = %s";
    datos=(int(_diassolicitados), int(_diassolicitados), _periodo, session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    okvacas= "Vacaciones Borradas correctamente"

    conexion=mysql.connect()
    sql = "Select id, empleado, date(desde), date(hasta), date(fecha_solicitud), estado, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = aprobador), fecha_aprobacion, case when estado in ('Aprobado','Rechazado') then 'hidden' else 'submit' end, case when estado in ('Aprobado','Rechazado') then '' else 'Eliminar' end, dias_totales, periodo from `vacaciones` where empleado = %s;"
    datos=(session["usuario"])
    stock = conexion.cursor()
    stock.execute(sql,datos)
    conexion.commit()

    return redirect("/vacaciones")


################################################
############ FIN VACACIONES ####################
################################################



@app.route('/masinfousuario', methods=['POST'])
def masinfousuario():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'masinfousuario',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _idusuario = request.form['idUsuario']

    return render_template("/sitio/masinfousuario.html", _idusuario=_idusuario)

@app.route('/masinfousuario2')
def masinfousuario2():

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from empleados where id_empleado = %s",session["usuario"])
    existe_datos=cursor.fetchall()
    conexion.commit
    hay_empleado = int(existe_datos[0][0])

    if hay_empleado > 0:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select `id`, `formacion`, `nacimiento`, `calle`, `nro`, `piso`, `depto`, `cp`, `localidad`, case when `provincia` = '' then 'Vacia' else provincia end, `foto`, `estado_civil`, `hijos` from empleados where id_empleado = %s",session["usuario"])
        datosusuarios=cursor.fetchall()
        conexion.commit
        return render_template("/sitio/masinfousuario.html", _idusuario=session["usuario"], datosusuarios = datosusuarios, boton = 'Actualizar')
    else:
        return render_template("/sitio/masinfousuario.html", _idusuario=session["usuario"], boton = 'Ingresar')


@app.route('/mas/infousuario', methods=['POST'])
def mas_infousuario():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'inserta_masinfousuario',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _fnacimiento = request.form['fnacimiento']
    _estadocivil = request.form['estadocivil']
    _hijos = request.form['hijos']
    _formacion = request.form['formacion']
    _calle = request.form['calle']
    _altura = request.form['altura']
    _piso = request.form['piso']
    _depto = request.form['depto']
    _localidad = request.form['localidad']
    _cp = request.form['cp']
    _provincia = request.form['provincia']

    sql = "delete from `empleados` where id_empleado = %s;"
    datos=(session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    sql = "INSERT INTO `empleados` (`id_empleado`, `formacion`, `nacimiento`, `calle`, `nro`, `piso`, `depto`, `localidad`, `cp`, `provincia`, `estado_civil`, `hijos`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s);"
    datos=(session["usuario"], _formacion, _fnacimiento, _calle, _altura, _piso, _depto, _localidad, _cp, _provincia, _estadocivil, _hijos)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    return redirect("/inicio")

##########################################
############ NOTICIAS ##############
##########################################
@app.route('/noticias')
def noticias():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'listado_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select *, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), case when apagar = 1 then 'btn btn-success btn-sm' else 'btn btn-warning btn-sm' end, case when apagar = 1 then 'Activar' else 'Apagar' end, case when apagar = 1 then 'activar' else 'apagar' end from noticias")
    noticias=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/noticias.html", noticias=noticias)


@app.route('/admin/noticias/guardar', methods=['POST'])
def admin_noticias_guardar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'guardar_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   



    _titulo = request.form['txtTitulo']
    _noticia = request.form['txtNoticia']
    _desarrollo = request.form['txtDesarrollo']
    _url = request.form['txtUrl']
    _fila = request.files['txtImagen']

    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')

    if _fila.filename!= "":
        nuevoNombre=horaActual+"_"+_fila.filename
        _fila.save("templates/sitio/img/"+nuevoNombre)

    sql = "INSERT INTO `noticias` (titulo,noticia,mas_noticia,link,imagen,creado_por,fecha,apagar) VALUES (%s, %s, %s, %s, %s, %s, %s,0);"
    datos=(_titulo,_noticia, _desarrollo, _url, nuevoNombre, session["usuario"], tiempo)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/noticias')


@app.route('/admin/noticias/borrar', methods=['POST'])
def admin_noticias_borrar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'borrar_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
    
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen from `noticias` WHERE id=%s", (_id))
    libro=cursor.fetchall()
    conexion.commit

    if os.path.exists("templates/sitio/img/"+str(libro[0][0])):
        os.unlink("templates/sitio/img/"+str(libro[0][0]))

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM `noticias` WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/noticias')



@app.route('/admin/noticias/apagar', methods=['POST'])
def admin_noticias_apagar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'apagar_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
    
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("update `noticias` set apagar = 1 WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/noticias')


@app.route('/admin/noticias/activar', methods=['POST'])
def admin_noticias_activar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'activar_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
    
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("update `noticias` set apagar = 0 WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/noticias')

##########################################
############ Gerencias ##############
##########################################
@app.route('/gerencias')
def gerencias():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'listar_gerencias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select *, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por) from gerencias")
    gerencias=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/gerencias.html", gerencias=gerencias)


@app.route('/admin/gerencias/guardar', methods=['POST'])
def admin_gerencias_guardar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'insertar_gerencias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   


    _gerencia = request.form['txtGerencia']
    
    tiempo = datetime.now()
    
    sql = "INSERT INTO `gerencias` (gerencia, creado_por, fecha) VALUES (%s, %s, %s);"
    datos=(_gerencia, session["usuario"], tiempo)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/gerencias')

@app.route('/admin/gerencias/borrar', methods=['POST'])
def admin_gerencias_apagar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'borrar_gerencias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from gerencias WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/gerencias')

##########################################
############ Jefaturas ##############
##########################################
@app.route('/jefaturas')
def jefaturas():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'listar_jefaturas',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   


    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select *, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por) from jefaturas")
    jefaturas=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select gerencia from gerencias")
    gerencias=cursor.fetchall()
    conexion.commit


    return render_template("/admin/jefaturas.html", gerencias=gerencias, jefaturas=jefaturas)


@app.route('/admin/jefaturas/guardar', methods=['POST'])
def admin_jefaturas_guardar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'guardar_jefaturas',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   


    _jefatura = request.form['txtJefatura']
    _gerencia = request.form['txtGerencia']
    
    tiempo = datetime.now()
    
    sql = "INSERT INTO `jefaturas` (jefatura, gerencia, creado_por, fecha) VALUES (%s, %s, %s, %s);"
    datos=(_jefatura, _gerencia, session["usuario"], tiempo)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/jefaturas')

@app.route('/admin/jefaturas/borrar', methods=['POST'])
def admin_jefaturas_borrar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'borrar_jefaturas',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from jefaturas WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/jefaturas')


@app.route('/organigrama')
def organigrama():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'organigrama',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   


    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT case when (select nivel from niveles where niveles.id = usuario.funcion and nivel not like 'Anal%') is null then '' else (select nivel from niveles where niveles.id = usuario.funcion and nivel not like 'Anal%') end, case when (select gerencia from gerencias where usuario.gerencia = gerencias.id) is null then '' else (select gerencia from gerencias where usuario.gerencia = gerencias.id) end, case when (select jefatura from jefaturas where usuario.jefatura = jefaturas.id) is null then '' else (select jefatura from jefaturas where usuario.jefatura = jefaturas.id) end, case when (select nivel from niveles where niveles.id = usuario.funcion and nivel like 'Anal%') is null then '' else (select nivel from niveles where niveles.id = usuario.funcion and nivel like 'Anal%') end, concat(nombre,' ',apellidos) FROM usuario where nombre_usuario not in ('dturconi') order BY concat(case when (select gerencia from gerencias where usuario.gerencia = gerencias.id) is null then '' else (select gerencia from gerencias where usuario.gerencia = gerencias.id) end, case when (select jefatura from jefaturas where usuario.jefatura = jefaturas.id) is null then '' else (select jefatura from jefaturas where usuario.jefatura = jefaturas.id) end, case when (select nivel from niveles where niveles.id = usuario.funcion and nivel like 'Anal%') is null then '' else (select nivel from niveles where niveles.id = usuario.funcion and nivel like 'Anal%') end)")
    organigrama=cursor.fetchall()
    conexion.commit

    return render_template("/admin/organigrama.html", organigrama = organigrama)

@app.route('/sitio/abrir_url', methods=['POST'])
def abrir_url():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'vacaciones_borrar',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _site = request.form['site']
    print(_site)
    google = webbrowser.Chrome(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    google.open_new_tab(_site)
    
    return redirect ("/inicio")

if __name__ == '__main__':
    app.run(debug=True)