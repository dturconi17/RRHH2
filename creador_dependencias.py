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


@app.route('/dependencias')
def dependencias():

    logs.logs1('Listar dependencia')   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, 
                    area,
                   (select estructura from estructuras where estructuras.id = area.id_estructura),
                   (select area from area area2 where area.id_dependencia = area2.id),
                    CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), 
                   id_estructura
                   from area""")
    dependencias=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select id, estructura from estructuras where id not in (1)")
    atribuciones=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select id, area from area")
    depende=cursor.fetchall()
    conexion.commit


    return render_template("/admin/dependencias.html", dependencias=dependencias, atribuciones=atribuciones, depende = depende)


@app.route('/admin/dependencias/guardar', methods=['POST'])
def admin_dependencias_guardar():

    logs.logs1('Guardar dependencia')

    _depende = request.form['txtDepende']
    _estructura = request.form['txtEstructura']
    _area = request.form['txtArea']

    tiempo = datetime.now()
    
    sql = "INSERT INTO `area` (area, id_dependencia, id_estructura, creado_por, fecha) VALUES (%s, %s, %s, %s, %s);"
    datos=(_area, _depende, _estructura, session["usuario"], tiempo)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/dependencias')

@app.route('/admin/dependencias/borrar', methods=['POST'])
def admin_dependencias_borrar():

    logs.logs1('Borrar dependencia')
    
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from area WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/dependencias')

@app.route('/admin/dependencias/editar', methods=['POST'])
def admin_dependencias_editar():

    logs.logs1('Editar dependencia')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, 
                    area,
                   (select estructura from estructuras where estructuras.id = area.id_estructura),
                   (select area from area area2 where area.id_dependencia = area2.id),
                    CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), 
                   id_estructura,
                   (select id from estructuras where estructuras.id = area.id_estructura),
                   (select id from area area2 where area.id_dependencia = area2.id)
                   from area where id = %s;""", (_id))
    dependencias=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select id, estructura from estructuras where id not in (1)")
    atribuciones=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select id, area from area")
    depende=cursor.fetchall()
    conexion.commit

    return render_template("/admin/dependencias_editar.html", dependencias=dependencias, atribuciones=atribuciones, depende = depende)

@app.route('/admin/dependencias/guardar_editar', methods=['POST'])
def admin_dependencias_guardar_editar():

    logs.logs1('Guardar Editar dependencias')

    _id = request.form['txtId']
    _area = request.form['txtArea']
    _estructura = request.form['txtEstructura']
    _depende = request.form['txtDepende']

    tiempo = datetime.now()
    
    sql = "update `area` set area = %s, id_dependencia = %s, id_estructura = %s, creado_por = %s, fecha = %s where id = %s;"
    datos=(_area, _depende, _estructura, session["usuario"], tiempo, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/dependencias')