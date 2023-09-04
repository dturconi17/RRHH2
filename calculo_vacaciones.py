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



@app.route('/cargarvacaciones')
def cargarvacaciones():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'cargarvacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()        
 
    tiempo = datetime.now().year

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select periodo, count(*), sum(dias_totales), sum(dias_tomados), sum(dias_pendientes), sum(dias_por_aprobarse), (select case when activo = 0 then 'Activar' else 'Ya activo' end from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo and periodos_activos.tipo_licencia = 'Vacaciones'), (select case when activo = 0 then 'btn btn-info btn-sm' else 'btn btn-success btn-sm' end from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo and periodos_activos.tipo_licencia = 'Vacaciones'), sum(dias_aprobados)  from stock_vacaciones group by periodo")
    calculo=cursor.fetchall()
    conexion.commit

    return render_template("/admin/cargarvacaciones.html", calculo = calculo, tiempo = tiempo)

@app.route('/cargarvacaciones/borrar', methods=['POST'])
def cargarvacaciones_borrar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'cargarvacaciones_borrar',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _periodo = request.form['Periodo']

    sql = "delete from `stock_vacaciones` where periodo = %s;"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,_periodo)
    conexion.commit()
    
    sql = "delete from periodos_activos where periodo = %s and tipo_licencia = 'Vacaciones';"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,_periodo)
    conexion.commit()
    

    return redirect("/cargarvacaciones")

@app.route('/cargarvacaciones/entrar', methods=['POST'])
def cargarvacaciones_entrar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'listar_vacaciones_por_empleado',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _periodo = request.form['Periodo']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT *, case when dias = 7 then 'Editar' else 'Revisar' end from stock_vacaciones where periodo = %s", (_periodo))
    listar=cursor.fetchall()
    conexion.commit

    return render_template("/admin/listar_empleado.html", listar = listar)



@app.route('/admin/cargarvacaciones/grabar', methods=['POST'])
def admin_cargarvacaciones_grabar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'admin_cargarvacaciones_grabar',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()        
 
    _Idvacaciones = request.form['Idvacaciones']
    _dias_totales = request.form['dias_totales']
    _dias_tomados = request.form['dias_tomados']
    _dias_pendientes = request.form['dias_pendientes']
    _dias_por_aprobarse = request.form['dias_por_aprobarse']
    _dias_aprobados = request.form['dias_aprobados']
    tiempo = datetime.now()

    sql = "update stock_vacaciones set dias_totales = %s, dias_tomados = %s, dias_pendientes = %s, dias_por_aprobarse = %s, usuario_modifica = %s, fecha_modifica = %s, dias_aprobados = %s where id = %s;"

    datos=(_dias_totales,_dias_tomados,_dias_pendientes, _dias_por_aprobarse, session["usuario"], tiempo, _dias_aprobados,_Idvacaciones)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/listarempleado")

@app.route('/alta_periodo')
def alta_periodo():
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'alta_periodo',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
    
    tiempo = datetime.now()

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("drop table periodo_nuevo")
    drop_periodo=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("create table periodo_nuevo as (SELECT year(now()) as periodo, nombre_usuario, year(now())-year(fecha_incorporacion) antiguedad, now() creacion, 0 dias FROM usuario where year(fecha_incorporacion) > 1900)")
    create_periodo=cursor.fetchall()
    conexion.commit

    sql = "update `periodo_nuevo` set `dias` = (SELECT dias from reglas_vacaciones where periodo_nuevo.antiguedad between reglas_vacaciones.desde and reglas_vacaciones.hasta)"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()

    sql = "delete from stock_vacaciones where periodo = year(now());"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()

    sql = "insert into stock_vacaciones (id_empleado, periodo, dias_totales, dias_tomados, dias_pendientes, dias_por_aprobarse, usuario_modifica, fecha_modifica, dias_aprobados) select nombre_usuario, cast(periodo as char), dias, 0, dias, 0, %s, now(), 0 from periodo_nuevo;"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, session["usuario"])
    conexion.commit()

    sql = "delete from periodos_activos where periodo = year(now()) and tipo_licencia = 'Vacaciones';"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()

    sql = "insert into periodos_activos (periodo, tipo_licencia, activo, creado_por, fecha) values (year(now()), 'Vacaciones',0,%s,%s);"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    datos=(session["usuario"], tiempo)
    cursor.execute(sql, datos)
    conexion.commit()


    return redirect("/cargarvacaciones")


@app.route('/listarvacaciones')
def listar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'listar_vacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT *, case when dias_totales < 8 then 'btn btn-warning btn-sm' else 'btn btn-info btn-sm' end, case when dias_totales < 8 then 'Revisar' else 'Editar' end from stock_vacaciones")
    listar=cursor.fetchall()
    conexion.commit

    return render_template("/admin/listar_vacaciones.html", listar = listar)


@app.route('/admin/vacaciones/borrar', methods=['POST'])
def admin_vacaciones_borrar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'borrar_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _id = request.form['Idvacaciones']
    print (_id)

    sql = "delete from stock_vacaciones where id = %s;"
    datos= (_id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    
    return redirect ("/listarvacaciones")


@app.route('/admin/vacaciones/grabar', methods=['POST'])
def admin_vacaciones_grabar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'grabar_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
 
    _Idvacaciones = request.form['Idvacaciones']
    _dias_totales = request.form['dias_totales']
    _dias_tomados = request.form['dias_tomados']
    _dias_pendientes = request.form['dias_pendientes']
    _dias_por_aprobarse = request.form['dias_por_aprobarse']
    _dias_aprobados = request.form['dias_aprobados']
    tiempo = datetime.now()

    sql = "update stock_vacaciones set dias_totales = %s, dias_tomados = %s, dias_pendientes = %s, dias_por_aprobarse = %s, usuario_modifica = %s, fecha_modifica = %s, dias_aprobados = %s where id = %s;"

    datos=(_dias_totales,_dias_tomados,_dias_pendientes, _dias_por_aprobarse, session["usuario"], tiempo, _dias_aprobados, _Idvacaciones)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/listarvacaciones")

@app.route('/admin/vacaciones/editar', methods=['POST'])
def admin_vacaciones_editar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'editar_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _id = request.form['Idvacaciones']

    sql = "select *, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = id_empleado), (select concat(day(fecha_incorporacion), '-', month(fecha_incorporacion),'-',year(fecha_incorporacion)) from usuario where nombre_usuario = id_empleado), concat(day(fecha_modifica), '-', month(fecha_modifica),'-',year(fecha_modifica)) from stock_vacaciones where id = %s;"
    datos=(_id)
    conexion= mysql.connect()
    editar = conexion.cursor()
    editar.execute(sql,datos)
    conexion.commit()

    return render_template("/admin/editar_vacaciones.html", editar = editar)

@app.route('/vacaciones_alta_empleado')
def admin_vacaciones_alta_empleado():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'alta_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    sql = "select distinct(periodo) from stock_vacaciones;"
    
    conexion= mysql.connect()
    periodo = conexion.cursor()
    periodo.execute(sql)
    conexion.commit()

    sql = "select concat(nombre, ' ', apellidos), nombre_usuario, concat(day(fecha_incorporacion), '-', month(fecha_incorporacion),'-',year(fecha_incorporacion)) from usuario group by concat(nombre , ' ' , apellidos), nombre_usuario;"
    
    conexion= mysql.connect()
    usuario = conexion.cursor()
    usuario.execute(sql)
    conexion.commit()


    return render_template("/admin/agregar_vacaciones.html", periodo = periodo, usuario = usuario)

@app.route('/admin/vacaciones/grabar_manual', methods=['POST'])
def admin_vacaciones_grabar_manual():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'grabado_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
 
    _IdEmpleado = request.form['IdEmpleado']
    _IdPeriodo = request.form['IdPeriodo']
    _dias_totales = request.form['dias_totales']
    _dias_tomados = request.form['dias_tomados']
    _dias_pendientes = request.form['dias_pendientes']
    _dias_por_aprobarse = request.form['dias_por_aprobarse']
    _dias_aprobados = request.form['dias_aprobados']
    tiempo = datetime.now()

    sql = "insert into stock_vacaciones (id_empleado, periodo, dias_totales, dias_tomados, dias_pendientes, dias_por_aprobarse, usuario_modifica, fecha_modifica, dias_aprobados) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    datos=(_IdEmpleado, _IdPeriodo, _dias_totales,_dias_tomados,_dias_pendientes, _dias_por_aprobarse, session["usuario"], tiempo, _dias_aprobados)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/listarvacaciones")

@app.route('/cargarvacaciones/activar', methods=['POST'])
def cargarvacaciones_activar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'activar_periodo_vacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    sql = "update `periodos_activos` set activo = 1 where periodo = 2023 and tipo_licencia = 'Vacaciones';"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()
    
    return redirect("/cargarvacaciones")
