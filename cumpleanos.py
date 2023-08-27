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

@app.route('/cumpleanos')
def cumpleanos():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'cumpleanos',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select (select concat(nombre,' ',apellidos) from usuario where empleados.id_empleado = nombre_usuario) cumpleanero, concat(day(nacimiento),'-',month(nacimiento),'-',year(nacimiento)) fecha_cumple, empleados.id_empleado, id_reply, id_recibe, mensaje, creador, fecha_alta, case when saludos.id_empleado != %s and mensaje is null then 'es_form' else 'no_es_form' end from empleados LEFT join saludos on empleados.id_empleado = saludos.id_recibe where concat(day(nacimiento),'-',month(nacimiento)) = concat(day(now()),'-',month(now()))", session["usuario"])
    datoscumplehoy=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select (select concat(nombre,' ',apellidos) from usuario where empleados.id_empleado = nombre_usuario) cumpleanero, concat(day(nacimiento),'-',month(nacimiento),'-',year(nacimiento)) fecha_cumple, empleados.id_empleado, id_reply, id_recibe, mensaje, creador, fecha_alta, case when mensaje is null then 'es_form' else 'no_es_form' end from empleados LEFT join saludos on empleados.id_empleado = saludos.id_recibe where concat(day(nacimiento),'-',month(nacimiento)) = concat(day(date_add(now(), interval 1 day)),'-',month(date_add(now(), interval 1 day)))")
    datoscumplemanana=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select (select concat(nombre,' ',apellidos) from usuario where id_empleado = nombre_usuario), concat(day(nacimiento),'-',month(nacimiento),'-',year(nacimiento)) from empleados where id_empleado != %s and concat(day(nacimiento),'-',month(nacimiento)) not in (concat(day(now()),'-',month(now())), concat(day(date_add(now(), interval 1 day)),'-',month(date_add(now(), interval 1 day))) ) order by month(nacimiento) asc, day(nacimiento) asc ", session["usuario"])
    datoscumple=cursor.fetchall()
    conexion.commit


    return render_template("/sitio/cumpleanos.html", datoscumplehoy = datoscumplehoy, datoscumplemanana = datoscumplemanana, datoscumple = datoscumple)

@app.route('/cumpleanos/mensaje', methods=['POST'])
def mensaje():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'envio_mensaje_cumple',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _usuario = request.form['Idusuario']
    _mensaje = request.form['mensaje']
    _tiempocal = datetime.now()
    
    sql = "insert into saludos (id_empleado, id_recibe, mensaje, creador, fecha_alta, visto) values (%s, %s, %s, %s, now(), 0);"
    datos= (session["usuario"], _usuario, _mensaje, session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    return redirect("/cumpleanos")

@app.route('/mensajes')
def mensajes():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'mensajes',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select mensaje, (select concat(nombre,' ',apellidos) from usuario where saludos.id_empleado = nombre_usuario) quien_envia, concat(day(fecha_alta),'-',month(fecha_alta),'-',year(fecha_alta)) fecha, id, id_empleado, case when mensaje is null then 'es_form' else 'no_es_form' end from saludos where visto = 0 and id_recibe = %s",session["usuario"])
    datosmensaje=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select mensaje, (select concat(nombre,' ',apellidos) from usuario where saludos.id_empleado = nombre_usuario) quien_envia, concat(day(fecha_alta),'-',month(fecha_alta),'-',year(fecha_alta)) fecha, id, id_empleado, case when mensaje is null then 'es_form' else 'no_es_form' end from saludos where visto = 1 and id_recibe = %s", session["usuario"])
    datosmensaje2=cursor.fetchall()
    conexion.commit

    sql = "update saludos set visto = 1 where visto = 0 and id_empleado = %s;"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    return render_template("/sitio/mensajes.html", datosmensaje = datosmensaje, datosmensaje2 = datosmensaje2)

@app.route('/cumpleanos/reply', methods=['POST'])
def reply_cumple():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'reply_envio_mensaje_cumple',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _idrecibe = request.form['Idrecibe']
    _mensaje = request.form['mensaje']
    _idreply = request.form['Idreply']    
    
    sql = "insert into saludos (id_reply, id_empleado, id_recibe, mensaje, creador, fecha_alta, visto) values (%s, %s, %s, %s, %s, now(), 0);"
    datos= (_idreply, session["usuario"], _idrecibe, _mensaje, session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    return redirect("/mensajes")