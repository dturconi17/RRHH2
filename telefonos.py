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

@app.route('/telefonos')
def telefonos():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'guia_telefonica',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    
    return render_template("/sitio/telefonos.html")

@app.route('/guia_telefonica')
def guia_telefonica():

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from datos_contacto where id_empleado = %s",session["usuario"])
    existe_datos=cursor.fetchall()
    conexion.commit
    hay_empleado = int(existe_datos[0][0])

    if hay_empleado > 0:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select `id`, `id_empleado`, `telefono_fijo`, `interno`, `celular`, `domicilio_laboral`, mail_laboral, `fecha` from datos_contacto where id_empleado = %s",session["usuario"])
        datosusuarios=cursor.fetchall()
        conexion.commit
        return render_template("/sitio/masinfoguia.html", _idusuario=session["usuario"], datosusuarios = datosusuarios, boton = 'Actualizar')
    else:
        return render_template("/sitio/masinfoguia.html", _idusuario=session["usuario"], boton = 'Ingresar')

@app.route('/mas/infocontacto', methods=['POST'])
def mas_infocontacto():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'inserta_masinfocontacto',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _telefono_fijo = request.form['telefono_fijo']
    _interno = request.form['interno']
    _celular = request.form['celular']
    _domicilio_laboral = request.form['domicilio_laboral']
    _mail = request.form['mail_laboral']
    
    sql = "delete from `datos_contacto` where id_empleado = %s;"
    datos=(session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    sql = "INSERT INTO `datos_contacto` (`id_empleado`, `telefono_fijo`, `interno`, `celular`, `domicilio_laboral`, `mail_laboral`, fecha) VALUES (%s, %s, %s, %s, %s, %s, now());"
    datos=(session["usuario"], _telefono_fijo, _interno, _celular, _domicilio_laboral, _mail)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    return redirect("/inicio")


@app.route('/buscar', methods=['POST'])
def buscar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'buscar_contacto',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _apellido = request.form['apellido']
    _apellido2 = "%rre%"
    pconexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select `id`, `id_empleado`, `telefono_fijo`, `interno`, `celular`, `domicilio_laboral`, mail_laboral, `fecha` from datos_contacto where id_empleado in (select nombre_usuario from usuario where apellidos like %s)",_apellido2)
    datosusuarios=cursor.fetchall()
    conexion.commit
    print (cursor.execute)
    return render_template("/sitio/telefonos.html", datosusuarios = datosusuarios)