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

@app.route('/obtener_arreglo_valores', methods=['GET'])
def obtener_arreglo_valores():
    try:
        # Establece una conexión a la base de datos
        conn = mysql.get_db()
        cursor = conn.cursor()

        # Realiza la consulta SQL para obtener un arreglo de valores
        cursor.execute("SELECT nivel FROM niveles")  # Cambia la consulta adecuadamente

        # Obtiene el resultado de la consulta
        resultados = cursor.fetchall()

        # Cierra la conexión y retorna los valores como un arreglo JSON
        cursor.close()

        valores = [resultado[0] for resultado in resultados]

        return jsonify({'valores': valores})

    except Exception as e:
        return str(e)


@app.route('/dependencias')
def dependencias():

    logs.logs1('Listar dependencias')   

    return render_template("/admin/dependencias.html")

@app.route('/dependencias_devuelve')
def dependencias_devuelve():

    logs.logs1('Listar dependencias')   

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

    return render_template("/admin/dependencias.html", gerencias=gerencias, atribuciones=atribuciones)