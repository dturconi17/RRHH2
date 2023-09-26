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


@app.route('/niveles')
def niveles():

    logs.logs1('Creador de Jerarquias')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, nivel, 
                   (select descripcion from orden where id_orden = niveles.orden),  
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por)
                   from niveles""")
    niveles=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id_orden, descripcion from orden""")
    orden=cursor.fetchall()
    conexion.commit

    return render_template("/admin/niveles.html", niveles = niveles, orden = orden)


@app.route('/admin/niveles/guardar', methods=['POST'])
def admin_niveles_guardar():

    logs.logs1('Guardar Jerarquias')

    _jerarquia = request.form['Jerarquia']
    _orden = request.form['Orden']

    tiempo = datetime.now()
    
    sql = "INSERT INTO `niveles` (nivel, orden, creado_por, fecha) VALUES (%s, %s, %s, %s);"
    datos=(_jerarquia, _orden, session["usuario"], tiempo)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/niveles')

@app.route('/admin/niveles/borrar', methods=['POST'])
def admin_niveles_borrar():
    
    logs.logs1('Borrar Niveles')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from niveles WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/niveles')

@app.route('/admin/niveles/guardar_editar', methods=['POST'])
def admin_niveles_guardar_editar():

    logs.logs1('Guardar Editar Niveles')

    _id = request.form['txtId']
    _jerarquia = request.form['Jerarquia']
    _orden = request.form['Orden']


    tiempo = datetime.now()
    
    sql = "update `niveles` set nivel = %s, orden = %s, creado_por = %s, fecha = %s where id = %s;"
    datos=(_jerarquia, _orden, session["usuario"], tiempo, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/niveles')

@app.route('/admin/niveles/editar', methods=['POST'])
def admin_niveles_editar():

    logs.logs1('Editar Empresa')

    _id = request.form['txtId']


    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, nivel, 
                   (select descripcion from orden where id_orden = niveles.orden),
                   orden,  
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por)
                  from niveles where id = %s;""", (_id))
    niveles=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id_orden, descripcion from orden""")
    orden=cursor.fetchall()
    conexion.commit

    return render_template("/admin/niveles_editar.html", niveles = niveles, orden = orden)