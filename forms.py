from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.core import DateField, SelectField, StringField, RadioField
from wtforms.fields.simple import PasswordField, SubmitField,HiddenField, TextAreaField
from wtforms.fields.html5 import DecimalRangeField
##from models import imagenes,usuario_final,usuario_administrador,usuario_superadmin

#Inicio formulario validación en Login#######################################################

class formlogin(FlaskForm):
    user = StringField('Usuario', validators=[validators.required(), validators.length(max=100)]) #Cómo se centra aquí?
    password = PasswordField('Contraseña', validators=[validators.required(), validators.length(max=100)])
    tipoUsuario = RadioField('Tipo de usuario', choices=[('UF','Usuario Final'),('A','Administrador'),('SA','Super Administrador')])
    enviar = SubmitField('Ingresar')

#Fin formulario validación en Login##########################################################
