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
import logs

@app.route('/cargos')
def cargos():

    logs.logs1('Creador de Cargo')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, cargo_general, cargo_sub, 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por)
                   from cargos""")
    empresas=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/cargos.html", empresas=empresas)

@app.route('/admin/cargo/guardar', methods=['POST'])
def admin_cargos_guardar():

    logs.logs1('Guardar Cargo')

    _empresa = request.form['txtEmpresa']
    _domicilio = request.form['txtDomicilio']
    _cuit = request.form['txtCuit']

    tiempo = datetime.now()
    
    sql = "INSERT INTO `empresas` (empresa, creado_por, fecha, domicilio, cuit) VALUES (%s, %s, %s, %s, %s);"
    datos=(_empresa, session["usuario"], tiempo, _domicilio, _cuit)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/empresa')

@app.route('/admin/cargo/guardar_editar', methods=['POST'])
def admin_cargos_guardar_editar():

    logs.logs1('Guardar Editar Cargo')

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

    return redirect('/cargo')

@app.route('/admin/cargo/borrar', methods=['POST'])
def admin_cargo_borrar():
    
    logs.logs1('Borrar Cargo')
 
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from empresas WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/cargo')

@app.route('/admin/cargo/editar', methods=['POST'])
def admin_cargo_editar():

    logs.logs1('Editar Cargo')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, empresa, 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por),
                   cuit,
                   domicilio
                   from empresas where id = %s;""", (_id))
    empresas=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/cargos_editar.html", empresas=empresas)