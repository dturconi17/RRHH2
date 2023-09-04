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

@app.route('/jefaturas')
def jefaturas():

    logs.logs1('Listar Jefatura')   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, jefatura,  
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), 
                   (select descripcion from aprobaciones where aprobaciones.id = jefaturas.aprobacion), 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha))
                   from jefaturas""")
    jefaturas=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select id, descripcion from aprobaciones")
    atribuciones=cursor.fetchall()
    conexion.commit

    return render_template("/admin/jefaturas.html", jefaturas=jefaturas, atribuciones=atribuciones)


@app.route('/admin/jefaturas/guardar', methods=['POST'])
def admin_jefaturas_guardar():

    logs.logs1('Guardar Jefatura')

    _jefatura = request.form['txtJefatura']
    _atribucion = request.form['txtAtribucion']
     
    tiempo = datetime.now()
    
    sql = "INSERT INTO `jefaturas` (jefatura, creado_por, fecha, aprobacion) VALUES (%s, %s, %s, %s);"
    datos=(_jefatura, session["usuario"], tiempo, _atribucion)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/jefaturas')

@app.route('/admin/jefaturas/borrar', methods=['POST'])
def admin_jefaturas_borrar():

    logs.logs1('Borrar Jefatura')
    
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from jefaturas WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/jefaturas')

@app.route('/admin/jefaturas/editar', methods=['POST'])
def admin_jefaturas_editar():

    logs.logs1('Editar Jefatura')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, jefatura,  
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), 
                   (select descripcion from aprobaciones where aprobaciones.id = jefaturas.aprobacion),
                   (select id from aprobaciones where aprobaciones.id = jefaturas.aprobacion), 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha))
                   from jefaturas where id = %s;""", (_id))
    jefaturas=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select id, descripcion from aprobaciones")
    atribuciones=cursor.fetchall()
    conexion.commit


    return render_template("/admin/jefaturas_editar.html", jefaturas = jefaturas, atribuciones = atribuciones)

@app.route('/admin/jefaturas/guardar_editar', methods=['POST'])
def admin_jefaturas_guardar_editar():

    logs.logs1('Guardar Editar Jefaturas')

    _id = request.form['txtId']
    _atribucion = request.form['txtAtribucion']
    _jefatura = request.form['txtJefatura']

    tiempo = datetime.now()
    
    sql = "update `jefaturas` set jefatura = %s, aprobacion = %s, creado_por = %s, fecha = %s where id = %s;"
    datos=(_jefatura, _atribucion, session["usuario"], tiempo, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/jefaturas')