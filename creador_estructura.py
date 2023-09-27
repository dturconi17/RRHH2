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
    cursor.execute("""Select id, 
                   area, 
                   (select nivel from niveles where tipo_area = niveles.id),
                   concat((select nivel from niveles where (select tipo_area from estructuras b where b.id=estructuras.reporta_a) = niveles.id), ' ',
                   (select area from estructuras b where b.id = estructuras.reporta_a)),  
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por)
                   from estructuras""")
    estructura=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select count(*) from estructuras """)
    reporta_cantidad=cursor.fetchall()
    conexion.commit
    cnt_reporta = int(reporta_cantidad[0][0])
    
    if cnt_reporta > 0:

        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("""Select id, nivel, orden from niveles where nivel not in ('Admin')""")
        jerarquia=cursor.fetchall()
        conexion.commit

        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("""Select id, concat((select nivel from sitio.niveles where id = tipo_area),' ',area) from estructuras """)
        reporta=cursor.fetchall()
        conexion.commit

        return render_template("/admin/estructura.html", estructura = estructura, jerarquia = jerarquia, combo_reporta = 'disponible', reporta=reporta)
    
    else:

        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("""Select id, nivel, orden from niveles where orden = 30""")
        jerarquia=cursor.fetchall()
        conexion.commit


        return render_template("/admin/estructura.html", estructura = estructura, jerarquia = jerarquia, combo_reporte = 'no disponible')



@app.route('/admin/estructura/guardar', methods=['POST'])
def admin_estructura_guardar():

    logs.logs1('Guardar estructura')

    _tipo_area = request.form['Tipo_area']
    _nombre_area = request.form['nombre_area']
    _reporta_a = request.form['reporta_a'] if 'reporta_a' in request.form else 0
    _nivel_area = 1
    tiempo = datetime.now()
    

    sql = "INSERT INTO `estructuras` (area, tipo_area, reporta_a, creado_por, fecha, nivel_area) VALUES (%s, %s, %s, %s, %s, %s);"
    datos=(_nombre_area, _tipo_area, _reporta_a, session["usuario"], tiempo, _nivel_area)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""update estructuras set nivel_area = (select orden from niveles where niveles.id = estructuras.tipo_area)""")
    jerarquia=cursor.fetchall()
    conexion.commit

    
    
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
    _jerarquia = request.form['Tipo_area']
    _nombre_area = request.form['nombre_area']
    _reporta_a = request.form['reporta_a']

    tiempo = datetime.now()
    
    sql = "update `estructuras` set tipo_area = %s, area = %s, reporta_a = %s, creado_por = %s, fecha = %s where id = %s;"
    datos=(_jerarquia, _nombre_area, _reporta_a, session["usuario"], tiempo, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""update estructuras set nivel_area = (select orden from niveles where niveles.id = estructuras.tipo_area)""")
    jerarquia=cursor.fetchall()
    conexion.commit

    return redirect('/estructura')

@app.route('/admin/estructura/editar', methods=['POST'])
def admin_estructura_editar():

    logs.logs1('Editar estructura')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, 
                   area, 
                   (select nivel from niveles where tipo_area = niveles.id),
                   tipo_area,
                   concat((select nivel from niveles where (select tipo_area from estructuras b where b.id=estructuras.reporta_a) = niveles.id), 
                   ' ',
                   (select area from estructuras b where b.id = estructuras.reporta_a)),  
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por),
                   (select id from estructuras c where estructuras.reporta_a = id )
                   from estructuras where id = %s;""", (_id))
    estructura=cursor.fetchall()
    conexion.commit
   
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, nivel, orden from niveles where nivel not in ('Admin')""")
    jerarquia=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, concat((select nivel from sitio.niveles where id = tipo_area),' ',area) from estructuras """)
    reporta=cursor.fetchall()
    conexion.commit


    return render_template("/admin/estructura_editar.html", estructura = estructura, jerarquia = jerarquia, reporta = reporta)