import os
from flask import Flask, jsonify
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime, timedelta
from flask import send_from_directory
from tkinter import *
from tkinter import messagebox
from django import template
from django.db import models
from db import *
import logs

@app.route('/estructura')
def estructura():

    logs.logs1('Creador de Estructura')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, estructura, '',  
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por)
                   from estructuras""")
    estructura=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/estructura.html", estructura = estructura)


@app.route('/admin/estructura/guardar', methods=['POST'])
def admin_estructura_guardar():

    logs.logs1('Guardar estructura')

    _aprobaciones = request.form['txtAprobacion']

    tiempo = datetime.now()
    
    sql = "INSERT INTO `estructuras` (estructura, creado_por, fecha, aprobacion) VALUES (%s, %s, %s, 15);"
    datos=(_aprobaciones, session["usuario"], tiempo)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/estructura')

@app.route('/admin/estructura/borrar', methods=['POST'])
def admin_estructura_borrar():
    
    logs.logs1('Borrar estructura')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from estructuras WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/estructura')

@app.route('/admin/estructura/guardar_editar', methods=['POST'])
def admin_estructura_guardar_editar():

    logs.logs1('Guardar Editar estructura')

    _id = request.form['txtId']
    _jerarquia = request.form['txtJerarquia']


    tiempo = datetime.now()
    
    sql = "update `estructuras` set estructura = %s, creado_por = %s, fecha = %s where id = %s;"
    datos=(_jerarquia, session["usuario"], tiempo, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/estructura')

@app.route('/admin/estructura/editar', methods=['POST'])
def admin_estructura_editar():

    logs.logs1('Editar estructura')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, estructura, '',  
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por)
                   from estructuras where id = %s;""", (_id))
    estructura=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/estructura_editar.html", estructura = estructura)