from os import name
from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask.templating import render_template
from forms import formlogin
from models import login
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


lista_usuarios = ["Diana", "Maryluz", "Edwin"]
lista_superAdministradores = ["Daniel", "Luis"]
lista_Administradores = ["Camila", "Juliana"]


@app.route('/', methods=["GET", "POST"])
def inicio():
    formulario =formlogin()
    return render_template('login.html', form=formulario)


@app.route("/registro", methods=["GET", "POST"])
def registrarse():
    return render_template('Register.html')


@app.route("/perfil", methods=["GET", "POST"])
def ir_a_perfil():
    return render_template('Perfil.html')


@app.route("/perfil/mensaje", methods=["GET", "POST"])
def mensaje():

    return render_template('Mensaje.html')


@app.route("/perfil/nuevoPost", methods=["GET", "POST"])
def newPost():
    return render_template('NewPublicacion.html')


@app.route("/perfil/opciones", methods=["GET", "POST"])
def option():
    return render_template('optionPost.html')


@app.route("/perfil/busqueda", methods=["GET", "POST"])
def users():
    return render_template("BusquedaUsuario.html")


@app.route("/super_administrador", methods=["GET", "POST"])
def superAdmin():
    return render_template("Dashboard_SuperAdministrador.html")


@app.route("/super_administrador/editar", methods=["GET", "POST"])
def editUsers():

    return render_template("EditarUsuario.html")


@app.route("/administrador", methods=["GET", "POST"])
def Admin():

    return render_template("Dashboard_Administrador.html")


@app.route("/administrador/publicacion", methods=["GET", "POST"])
def AdminPost():
    return render_template("optionPost_admin.html")


@app.route("/administrador/editar", methods=["GET", "POST"])
def AdminEditUser():
    return render_template("EditarUsuario_permisosAdmin.html")


@app.route("/perfil/comentarios", methods=["GET", "POST"])
def comentario():
    return render_template("Comentarios.html")


@app.route("/perfil/nuevo", methods=["GET", "POST"])
def newComentario():
    return render_template("AddComent.html")
# ***************************************************************************

@app.route('/login/', methods=['GET', 'POST'])
def usuario_registrado():
    if request.method =="GET":
        formulario =formlogin()
        return render_template('login.html', form=formulario)
    else:
        formulario = formlogin(request.form)

        usr = formulario.user.data.replace("'","")
        pwd = formulario.password.data.replace("'","")
        
        obj_login = login(usr,pwd,"","","")
        objeto_login =login.cargar(formulario.user.data)

        if(objeto_login==None):
            return render_template('login.html', mensaje="Nombre de usuario o contraseña incorrecta.", 
            form=formulario)
        else:
            session['id_usuario_logueado'] = objeto_login.id_usuario
            print(formulario.tipoUsuario.data)
            if obj_login.autenticar() and formulario.tipoUsuario.data == "UF" and formulario.tipoUsuario.data==objeto_login.tipo_usuario: 
                # session.clear() 
                session["nombre_usuario"] = usr
                return redirect( url_for('registrado_UF'))

            elif obj_login.autenticar() and formulario.tipoUsuario.data == "SA" and formulario.tipoUsuario.data==objeto_login.tipo_usuario: 
                # session.clear()
                session["nombre_usuario"] = usr
                return redirect( url_for('registrado_SA'))
 
            elif obj_login.autenticar() and formulario.tipoUsuario.data == "A" and formulario.tipoUsuario.data==objeto_login.tipo_usuario:     
                # session.clear()
                session["nombre_usuario"] = usr
                return redirect( url_for('registrado_A'))
            else:
                return render_template('login.html', mensaje="Nombre de usuario o contraseña incorrecta.", 
            form=formulario)


@app.route('/usuario_final_registrado/', methods=['GET', 'POST'])
def registrado_UF():
    if request.method =="GET":
        formulario =formlogin()
        return render_template('Perfil.html', form=formulario)

@app.route('/opciones_super_administrador/', methods=['GET', 'POST'])
def registrado_SA():
    if request.method =="GET":
        formulario =formlogin()
        return render_template('Perfil.html', form=formulario)

@app.route('/opciones_administrador/', methods=['GET', 'POST'])
def registrado_A():
    if request.method =="GET":
        formulario =formlogin()
        return render_template('Perfil.html', form=formulario)
