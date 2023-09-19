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


@app.route('/gerencias')
def gerencias():

    logs.logs1('Listar Gerencia')   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, gerencia,  
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), 
                   (select descripcion from aprobaciones where aprobaciones.id = gerencias.aprobacion), 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha))
                   from gerencias""")
    gerencias=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select id, descripcion from aprobaciones")
    atribuciones=cursor.fetchall()
    conexion.commit

    return render_template("/admin/gerencias.html", gerencias=gerencias, atribuciones=atribuciones)


@app.route('/admin/gerencias/guardar', methods=['POST'])
def admin_gerencias_guardar():

    logs.logs1('Guardar Gerencia')

    _gerencia = request.form['txtGerencia']
    _atribucion = request.form['txtAtribucion']
     
    tiempo = datetime.now()
    
    sql = "INSERT INTO `gerencias` (gerencia, creado_por, fecha, aprobacion) VALUES (%s, %s, %s, %s);"
    datos=(_gerencia, session["usuario"], tiempo, _atribucion)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/gerencias')

@app.route('/admin/gerencias/borrar', methods=['POST'])
def admin_gerencias_borrar():

    logs.logs1('Borrar Gerencia')
    
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from gerencias WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/gerencias')

@app.route('/admin/gerencias/editar', methods=['POST'])
def admin_gerencias_editar():

    logs.logs1('Editar Gerencia')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, 
                   gerencia,  
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), 
                   (select descripcion from aprobaciones where aprobaciones.id = gerencias.aprobacion),
                   (select id from aprobaciones where aprobaciones.id = gerencias.aprobacion), 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha))
                   from gerencias where id = %s;""", (_id))
    gerencias=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select id, descripcion from aprobaciones")
    atribuciones=cursor.fetchall()
    conexion.commit


    return render_template("/admin/gerencias_editar.html", gerencias = gerencias, atribuciones = atribuciones)

@app.route('/admin/gerencias/guardar_editar', methods=['POST'])
def admin_gerencias_guardar_editar():

    logs.logs1('Guardar Editar Gerencias')

    _id = request.form['txtId']
    _atribucion = request.form['txtAtribucion']
    _gerencia = request.form['txtGerencia']

    tiempo = datetime.now()
    
    sql = "update `gerencias` set gerencia = %s, aprobacion = %s, creado_por = %s, fecha = %s where id = %s;"
    datos=(_gerencia, _atribucion, session["usuario"], tiempo, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/gerencias')