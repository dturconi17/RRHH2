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

    logs.logs1('Creador de Niveles')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, nivel, '',  
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por)
                   from niveles""")
    niveles=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/niveles.html", niveles = niveles)


@app.route('/admin/niveles/guardar', methods=['POST'])
def admin_niveles_guardar():

    logs.logs1('Guardar Niveles')

    _aprobaciones = request.form['txtAprobacion']

    tiempo = datetime.now()
    
    sql = "INSERT INTO `niveles` (nivel, creado_por, fecha) VALUES (%s, %s, %s);"
    datos=(_aprobaciones, session["usuario"], tiempo)
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
    _empresa = request.form['txtEmpresa']
    _domicilio = request.form['txtDomicilio']
    _cuit = request.form['txtCuit']

    tiempo = datetime.now()
    
    sql = "update `empresas` set empresa = %s, creado_por = %s, fecha = %s, domicilio = %s, cuit = %s where id = %s;"
    datos=(_empresa, session["usuario"], tiempo, _domicilio, _cuit, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/empresa')

@app.route('/admin/niveles/editar', methods=['POST'])
def admin_niveles_editar():

    logs.logs1('Editar Empresa')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, empresa, 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por),
                   cuit,
                   domicilio
                   from empresas where id = 1""")
    empresas=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/empresas_editar.html", empresas=empresas)