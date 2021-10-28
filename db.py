# Aquí se desarrollan todas las funciones que tienen que ver con la conexión de la base de datos
# No es necesario sectorizar por tipo CRUD

import sqlite3

from sqlite3 import Error



# INICIO FUNCION PARA ESTABLECER CONEXION CON BASE DE DATOS ####################################

def conectar():
    try:
        conn = sqlite3.connect('db/redsocial.db')
        return conn
    except Error as err:
        print("Ocurrió un error al establecer la conexión: " + str(err))
        return None
# FIN FUNCION PARA ESTABLECER CONEXION CON BASE DE DATOS #######################################

# INICIO FUNCION PARA EJECUTAR SQL DE TIPO INSERT, UPDATE, DELETE ##############################
def ejecutar_insert(_sql, lista_parametros):
    try:
        conn = conectar() #Conectamos a la BD
        if conn:
            #Creamos el objeto cursor para ejecutar SQL
            objeto_cursor = conn.cursor() 
            #Invocamos el metodo execute del cursor para ejecutar el comando
            #rowcount nos devuelve la cantidad de filas afectadas por el comando.
            filas = objeto_cursor.execute(_sql, lista_parametros).rowcount 
            #Cerramos el cursor
            objeto_cursor.close()
            #Confirmamos los cambios realizados por el cursor
            conn.commit()
            #Cerramos la conexion
            conn.close()
            return filas #retornamos la cantidad de filas afectadas.
        else:
            print("No se pudo establecer la conexión. Ver errores previos.")
            return -1
    except Error as err:
        print("Ocurrió un error al intentar ejecutar el comando: " + _sql + " - " + str(err))
        return -1
# FIN FUNCION PARA EJECUTAR SQL DE TIPO INSERT, UPDATE, DELETE #################################

# INICIO FUNCION PARA EJECUTAR LOS SQL DE TIPO SELECT ##########################################
def ejecutar_select(_sql, lista_pametros):
    try:
        #Establecemos la conexión
        conn = conectar()
        if conn:
            #Forzamos la conversión de los resultados de select
            #de lista de tuplas a lista de diccionarios
            conn.row_factory = fabrica_diccionarios
            #Creamos el objeto cursor para ejecutar los comandos
            objeto_cursor = conn.cursor()
            #Si hay parametros invocamos execute con la lista de parametros
            if lista_pametros:
                objeto_cursor.execute(_sql, lista_pametros)
            else:
                #Se ejecuta la instrucción sin parámetros
                objeto_cursor.execute(_sql)
            #Se devuelven las filas de la consulta en una lista
            #se almacenan en la variable filas.
            filas = objeto_cursor.fetchall()
            objeto_cursor.close()
            conn.close()
            return filas
        else:
            print("No se pudo establecer la conexión. Ver errores previos.")
            return None
    except Error as err:
        print("Ocurrió un error al intentar ejecutar el comando: " + _sql + " - " + str(err))
        return None
# FIN FUNCION PARA EJECUTAR LOS SQL DE TIPO SELECT #############################################

# INICIO FUNCION PARA CONVERTIR TUPLAS EN DICCIONARIOS #########################################
def fabrica_diccionarios(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
# FIN FUNCION PARA CONVERTIR TUPLAS EN DICCIONARIOS ############################################
