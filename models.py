import db

from werkzeug.security import generate_password_hash, check_password_hash

# Aquí se desarrollan todas las funciones que tienen que ver con la conexión de la base de datos
# Es necesario sectorizar por tipo CRUD

# INICIO CLASES Y FUNCIONES RELACIONADAS CON EL CRUD IMAGENES ##################################

class imagenes():
    id_imagen = 0
    nombre_imagen =''
    id_usuario = ''
    fecha = ''
    

    def __init__(self, pid_imagen, pnombre_imagen, pid_usuario,
                 pfecha):

        self.id_imagen = pid_imagen
        self.nombre_imagen = pnombre_imagen
        self.id_usuario = pid_usuario
        self.fecha = pfecha
       

    @classmethod
    def cargar(cls, pid_imagen):
        sql = "SELECT * FROM tbl_imagenes WHERE id_imagen = ?;"
        resultado = db.ejecutar_select(sql, [ pid_imagen ])
        if resultado:
            if len(resultado)>0:
                return cls(pid_imagen, resultado[0]["nombre_imagen"], 
                resultado[0]["id_usuario"], resultado[0]["fecha"])
        
        return None

    def insertar(self):
        sql = "INSERT INTO tbl_imagenes (nombre_imagen, id_usuario, fecha,) VALUES (?,?,?);"
        afectadas = db.ejecutar_insert(sql, [self.nombre_imagen, self.id_usuario, self.fecha])
        return ( afectadas > 0 )

    def eliminar(self): 
        sql = "DELETE FROM tbl_imagenes WHERE id_imagen = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.id_imagen])
        return ( afectadas > 0 )
    
    def actualizar(self):
        sql = "UPDATE tbl_imagenes SET nombre_imagen =? , fecha = ? WHERE id_imagen = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.nombre_imagen, self.fecha, self.id_imagen ])
        return ( afectadas > 0 ) 





#Si se necesitan más métodos estáticos podría ser en Gestión 
    #@staticmethod
    # FIN CLASES Y FUNCIONES RELACIONADAS CON EL CRUD  #####################################
# Inicio Logueo en la aplicacion
class login():
    usuario=''
    contrasena=''
    tipo_usuario=''
    activo=''
    id_usuario=0

    def __init__(self, pusuario, pcontrasena ,ptipo_usuario , pactivo,pid_usuario) -> None:
       self.usuario=pusuario
       self.contrasena=pcontrasena
       self.tipo_usuario=ptipo_usuario
       self.activo=pactivo
       self.id_usuario=pid_usuario

    def autenticar(self):
        #Este query es inseguro porque puede permitir una inyección SQL
        #Para mitigar usamos comandos SQL parametrizados
        sql = "SELECT * FROM tbl_usuarios WHERE nick_usuario = ?;"
        obj = db.ejecutar_select(sql, [ self.usuario ])
        if obj:
            if len(obj) >0:
                #Agregamos la invocación al metodo check_password_hash
                #para verificar el password digitado contra el hash seguro almacenado en bd.
                if check_password_hash(obj[0]["contrasena"], self.contrasena):
                    return True
        
        return False        

    @classmethod
    def cargar(cls, usuario):
        sql = "SELECT * FROM tbl_usuarios WHERE nick_usuario = ? ;"
        #sql = "SELECT * FROM tbl_usuarios WHERE usuario = ? AND contrasena = ? AND tipo_usuario=? AND activo='SI';"
        resultado = db.ejecutar_select(sql, [usuario])
        if resultado:
            if len(resultado)>0:
                return cls(resultado[0]["nick_usuario"], '********', resultado[0]["tipo_usuario"],'SI', resultado[0]["id_usuario"])
                #return cls(pusuario, pcontrasena, ptipo_usuario,'SI', resultado[0]["id_usuario"])
        return None

    @staticmethod
    def datos_usuario_logueado(id_usuario):
        sql = "SELECT * FROM tbl_usuarios WHERE id_usuario="+str(id_usuario)+";"
        return db.ejecutar_select(sql, None)
    
# Fin Logueo en la aplicacion

# Tipos de Usuario:
# Inicio Clase Usuario Final  *************************************
class usuario_final():
    id_usuario=0
    documento=''
    nombres=''
    contrasena=''
    tipo_usuario='UF'
    activo='SI'
    usuario=''

    def __init__(self, pid_usuario, pdocumento,  pnombres, pcontrasena ,ptipo_usuario , pactivo, pusuario) -> None:
       self.id_usuario=pid_usuario
       self.documento=pdocumento
       self.nombres=pnombres
       self.contrasena=pcontrasena
       self.tipo_usuario=ptipo_usuario
       self.activo=pactivo
       self.usuario=pusuario
    
    @classmethod
    def cargar(cls, pid_usuario):
        sql = "SELECT * FROM tbl_usuarios WHERE id_usuario = ?;"
        resultado = db.ejecutar_select(sql, [ pid_usuario ])
        if resultado:
            if len(resultado)>0:
                return cls(pid_usuario, resultado[0]["documento"], 
                resultado[0]["nombres"], '********',
                resultado[0]["tipo_usuario"], resultado[0]["activo"], resultado[0]["usuario"])
                #Se cambia el campo contraseña para que no la muestre en las consultas
                #En la tabla usuarios se actualiza la logintud máxima permitida a 500
                #return cls(pid_usuario, resultado[0]["documento"], 
                #resultado[0]["nombres"], resultado[0]["contrasena"],
                #resultado[0]["tipo_usuario"], resultado[0]["activo"], resultado[0]["usuario"])
        return None

    def insertar(self):
        sql = "INSERT INTO tbl_usuarios (documento,nombres,contrasena,tipo_usuario,activo,usuario) VALUES (?,?,?,?,?,?);"
        hashed_pwd = generate_password_hash(self.contrasena, method='pbkdf2:sha256', salt_length=32)
        #Se ingresa la sentencia generate_password_hash para cifrar la contraseña que se envía a la base de datos
        afectadas = db.ejecutar_insert(sql, [self.documento, self.nombres, hashed_pwd, self.tipo_usuario, self.activo, self.usuario])
        return ( afectadas > 0 )

    def eliminar(self):
        sql = "DELETE FROM tbl_usuarios WHERE id_usuario = ?;"
        #sql = "DELETE FROM tbl_usuarios WHERE id_usuario = "+self.id_usuario+";"
        afectadas = db.ejecutar_insert(sql, [ self.id_usuario ])
        return ( afectadas > 0 )

    def modificar(self): # Aquí falta hacer un cambio para cifrar la consulta y el ingreso de la contraseña
        sql = "UPDATE tbl_usuarios SET documento = ?, nombres = ?, contrasena = ?, tipo_usuario = ?, activo = ?, usuario = ? WHERE id_usuario = ?;"
        hashed_pwd = generate_password_hash(self.contrasena, method='pbkdf2:sha256', salt_length=32)
        #Se ingresa la sentencia generate_password_hash para cifrar la contraseña que se envía a la base de datos
        afectadas = db.ejecutar_insert(sql, [ self.documento, self.nombres, hashed_pwd, self.tipo_usuario, self.activo, self.usuario , self.id_usuario])
        return ( afectadas > 0 )
    
    @staticmethod
    def listado():
        sql = "SELECT * FROM tbl_usuarios WHERE tipo_usuario='UF' ORDER BY id_usuario;"
        return db.ejecutar_select(sql, None)
# Fin Clase Usuario Final  *************************************************************************************************************************************
# Inicio Clase Usuario Administrador  **************************************************************************************************************************
class usuario_administrador():
    id_usuario=0
    documento=''
    nombres=''
    contrasena=''
    tipo_usuario='A'
    activo='SI'
    usuario=''

    def __init__(self, pid_usuario, pdocumento,  pnombres, pcontrasena ,ptipo_usuario , pactivo, pusuario) -> None:
       self.id_usuario=pid_usuario
       self.documento=pdocumento
       self.nombres=pnombres
       self.contrasena=pcontrasena
       self.tipo_usuario=ptipo_usuario
       self.activo=pactivo
       self.usuario=pusuario
    
    @classmethod
    def cargar(cls, pid_usuario):
        sql = "SELECT * FROM tbl_usuarios WHERE id_usuario = ?;"
        resultado = db.ejecutar_select(sql, [ pid_usuario ])
        if resultado:
            if len(resultado)>0:
                return cls(pid_usuario, resultado[0]["documento"], 
                resultado[0]["nombres"], '********',
                resultado[0]["tipo_usuario"], resultado[0]["activo"], resultado[0]["usuario"])
                #Se cambia el campo contraseña para que no la muestre en las consultas
                #En la tabla usuarios se actualiza la logintud máxima permitida a 500
                #return cls(pid_usuario, resultado[0]["documento"], 
                #resultado[0]["nombres"], resultado[0]["contrasena"],
                #resultado[0]["tipo_usuario"], resultado[0]["activo"], resultado[0]["usuario"])
        return None

    def insertar(self):
        sql = "INSERT INTO tbl_usuarios (documento,nombres,contrasena,tipo_usuario,activo,usuario) VALUES (?,?,?,?,?,?);"
        hashed_pwd = generate_password_hash(self.contrasena, method='pbkdf2:sha256', salt_length=32)
        #Se ingresa la sentencia generate_password_hash para cifrar la contraseña que se envía a la base de datos
        afectadas = db.ejecutar_insert(sql, [self.documento, self.nombres, hashed_pwd, self.tipo_usuario, self.activo, self.usuario])
        return ( afectadas > 0 )

    def eliminar(self): 
        sql = "DELETE FROM tbl_usuarios WHERE id_usuario = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.id_usuario ])
        return ( afectadas > 0 )

    def modificar(self):# Aquí falta hacer un cambio para cifrar la consulta y el ingreso de la contraseña
        sql = "UPDATE tbl_usuarios SET documento = ?, nombres = ?, contrasena = ?, tipo_usuario = ?, activo = ?, usuario = ? WHERE id_usuario = ?;"
        hashed_pwd = generate_password_hash(self.contrasena, method='pbkdf2:sha256', salt_length=32)
        #Se ingresa la sentencia generate_password_hash para cifrar la contraseña que se envía a la base de datos
        afectadas = db.ejecutar_insert(sql, [ self.documento, self.nombres, hashed_pwd, self.tipo_usuario, self.activo, self.usuario , self.id_usuario])
        return ( afectadas > 0 )
    
    @staticmethod
    def listado():
        sql = "SELECT * FROM tbl_usuarios WHERE tipo_usuario='A' ORDER BY id_usuario;"
        return db.ejecutar_select(sql, None)        
# Fin Clase Usuario Administrador  **************************************************************************************************************************

# FIN CLASES Y FUNCIONES RELACIONADAS CON EL CRUD USUARIOS #####################################
