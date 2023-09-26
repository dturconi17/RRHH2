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
from telefonos import *
from cumpleanos import *
import webbrowser
from creador_empresa import *
from creador_niveles import *
from creador_jefaturas import *
from creador_gerencias import *
from creador_reglas_vacaciones import *
from creador_dependencias import *
from creador_estructura import *
from creador_cargo import *

@app.route("/css/<archivocss>")
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/sitio/css'),archivocss)

@app.route('/')
def inicio():
    return render_template("/sitio/index.html")


@app.route('/admin_inicio')
def admin_inicio():

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from empresas")
    empresas=cursor.fetchall()
    conexion.commit
    cnt_empresas = int(empresas[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from niveles where id not in (99)")
    niveles=cursor.fetchall()
    conexion.commit
    cnt_niveles = int(niveles[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from reglas_vacaciones")
    reglas=cursor.fetchall()
    conexion.commit
    cnt_reglas = int(reglas[0][0])
    print (cnt_reglas)

    return render_template("admin/index.html", cnt_niveles = cnt_niveles, cnt_empresas = cnt_empresas, cnt_reglas = cnt_reglas)


@app.route('/inicio')
def inicio2():
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select * from noticias where apagar is null or apagar = 0")
    noticias=cursor.fetchall()
    conexion.commit
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from empleados where id_empleado = %s",(session["usuario"]))
    dato_usuario=cursor.fetchall()
    conexion.commit
    cnt_datos = int(dato_usuario[0][0])    
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from datos_contacto where id_empleado = %s",(session["usuario"]))
    dato_contacto=cursor.fetchall()
    conexion.commit
    cnt_contacto = int(dato_contacto[0][0])

    return render_template("sitio/inicio.html", noticias=noticias, cnt_datos = cnt_datos, cnt_contacto = cnt_contacto)


@app.route('/administrador')
def administrador():
    if not 'login' in session:
        return redirect("login")

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from empresas")
    empresas=cursor.fetchall()
    conexion.commit
    cnt_empresas = int(empresas[0][0])


    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from niveles where id not in (99)")
    niveles=cursor.fetchall()
    conexion.commit
    cnt_niveles = int(niveles[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from reglas_vacaciones")
    reglas=cursor.fetchall()
    conexion.commit
    cnt_reglas = int(reglas[0][0])

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from usuario where funcion not in (99)")
    usuario=cursor.fetchall()
    conexion.commit
    cnt_usuario = int(usuario[0][0])

    return render_template("/admin/index.html", cnt_niveles = cnt_niveles, cnt_empresas = cnt_empresas, cnt_reglas = cnt_reglas, cnt_usuario = cnt_usuario)

@app.route('/img/<imagen>')
def imagenes(imagen):
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)

@app.route('/masinfousuario', methods=['POST'])
def masinfousuario():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'masinfousuario',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _idusuario = request.form['idUsuario']

    return render_template("/sitio/masinfousuario.html", _idusuario=_idusuario)

@app.route('/masinfousuario2')
def masinfousuario2():

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select count(*) from empleados where id_empleado = %s",session["usuario"])
    existe_datos=cursor.fetchall()
    conexion.commit
    hay_empleado = int(existe_datos[0][0])

    if hay_empleado > 0:
        conexion=mysql.connect()
        cursor=conexion.cursor()
        cursor.execute("Select `id`, `formacion`, `nacimiento`, `calle`, `nro`, `piso`, `depto`, `cp`, `localidad`, case when `provincia` = '' then 'Vacia' else provincia end, `foto`, `estado_civil`, `hijos` from empleados where id_empleado = %s",session["usuario"])
        datosusuarios=cursor.fetchall()
        conexion.commit
        return render_template("/sitio/masinfousuario.html", _idusuario=session["usuario"], datosusuarios = datosusuarios, boton = 'Actualizar')
    else:
        return render_template("/sitio/masinfousuario.html", _idusuario=session["usuario"], boton = 'Ingresar')


@app.route('/mas/infousuario', methods=['POST'])
def mas_infousuario():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'inserta_masinfousuario',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _fnacimiento = request.form['fnacimiento']
    _estadocivil = request.form['estadocivil']
    _hijos = request.form['hijos']
    _formacion = request.form['formacion']
    _calle = request.form['calle']
    _altura = request.form['altura']
    _piso = request.form['piso']
    _depto = request.form['depto']
    _localidad = request.form['localidad']
    _cp = request.form['cp']
    _provincia = request.form['provincia']

    sql = "delete from `empleados` where id_empleado = %s;"
    datos=(session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    sql = "INSERT INTO `empleados` (`id_empleado`, `formacion`, `nacimiento`, `calle`, `nro`, `piso`, `depto`, `localidad`, `cp`, `provincia`, `estado_civil`, `hijos`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s);"
    datos=(session["usuario"], _formacion, _fnacimiento, _calle, _altura, _piso, _depto, _localidad, _cp, _provincia, _estadocivil, _hijos)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    return redirect("/inicio")

##########################################
############ NOTICIAS ##############
##########################################
@app.route('/noticias')
def noticias():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'listado_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select *, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), case when apagar = 1 then 'btn btn-success btn-sm' else 'btn btn-warning btn-sm' end, case when apagar = 1 then 'Activar' else 'Apagar' end, case when apagar = 1 then 'activar' else 'apagar' end from noticias")
    noticias=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/noticias.html", noticias=noticias)


@app.route('/admin/noticias/guardar', methods=['POST'])
def admin_noticias_guardar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'guardar_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   



    _titulo = request.form['txtTitulo']
    _noticia = request.form['txtNoticia']
    _desarrollo = request.form['txtDesarrollo']
    _url = request.form['txtUrl']
    _fila = request.files['txtImagen']

    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')

    if _fila.filename!= "":
        nuevoNombre=horaActual+"_"+_fila.filename
        _fila.save("templates/sitio/img/"+nuevoNombre)

    sql = "INSERT INTO `noticias` (titulo,noticia,mas_noticia,link,imagen,creado_por,fecha,apagar) VALUES (%s, %s, %s, %s, %s, %s, %s,0);"
    datos=(_titulo,_noticia, _desarrollo, _url, nuevoNombre, session["usuario"], tiempo)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/noticias')


@app.route('/admin/noticias/borrar', methods=['POST'])
def admin_noticias_borrar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'borrar_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
    
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen from `noticias` WHERE id=%s", (_id))
    libro=cursor.fetchall()
    conexion.commit

    if os.path.exists("templates/sitio/img/"+str(libro[0][0])):
        os.unlink("templates/sitio/img/"+str(libro[0][0]))

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM `noticias` WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/noticias')



@app.route('/admin/noticias/apagar', methods=['POST'])
def admin_noticias_apagar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'apagar_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
    
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("update `noticias` set apagar = 1 WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/noticias')


@app.route('/admin/noticias/activar', methods=['POST'])
def admin_noticias_activar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'activar_noticias',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
    
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("update `noticias` set apagar = 0 WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/noticias')


@app.route('/organigrama')
def organigrama():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'organigrama',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   


    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT case when (select nivel from niveles where niveles.id = usuario.funcion and nivel not like 'Anal%') is null then '' else (select nivel from niveles where niveles.id = usuario.funcion and nivel not like 'Anal%') end, case when (select gerencia from gerencias where usuario.gerencia = gerencias.id) is null then '' else (select gerencia from gerencias where usuario.gerencia = gerencias.id) end, case when (select jefatura from jefaturas where usuario.jefatura = jefaturas.id) is null then '' else (select jefatura from jefaturas where usuario.jefatura = jefaturas.id) end, case when (select nivel from niveles where niveles.id = usuario.funcion and nivel like 'Anal%') is null then '' else (select nivel from niveles where niveles.id = usuario.funcion and nivel like 'Anal%') end, concat(nombre,' ',apellidos) FROM usuario where nombre_usuario not in ('dturconi') order BY concat(case when (select gerencia from gerencias where usuario.gerencia = gerencias.id) is null then '' else (select gerencia from gerencias where usuario.gerencia = gerencias.id) end, case when (select jefatura from jefaturas where usuario.jefatura = jefaturas.id) is null then '' else (select jefatura from jefaturas where usuario.jefatura = jefaturas.id) end, case when (select nivel from niveles where niveles.id = usuario.funcion and nivel like 'Anal%') is null then '' else (select nivel from niveles where niveles.id = usuario.funcion and nivel like 'Anal%') end)")
    organigrama=cursor.fetchall()
    conexion.commit

    return render_template("/admin/organigrama.html", organigrama = organigrama)

@app.route('/sitio/abrir_url', methods=['POST'])
def abrir_url():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'vacaciones_borrar',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _site = request.form['site']
    print(_site)
    google = webbrowser.Chrome(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    google.open_new_tab(_site)
    
    return redirect ("/inicio")

if __name__ == '__main__':
    app.run(debug=True)