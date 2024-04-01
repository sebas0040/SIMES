#importacion del modulo
import psycopg2,os,sys
class DataBase():
    
    def __init__(self) -> None:
        # Conexion a base de datos
        self.conn = psycopg2.connect(user='postgres', password = 'POSTGRES1',host='127.0.0.1', port='5432', database='db_Simes')
        # Utilizar cursor
        self.dir_simes = os.path.dirname(os.path.dirname(__file__)) # Es la ruta del directorio simes
                                                                    # se usa para aceder a los archivos de todo el programa
                                                                    # sin complicaciones de importación 
        self.cur = self.conn.cursor()
        self.llenar_base_datos_usuario() # se inicializa para tener Usuarios en el programa
            

    def __del__(self):
        # Cerrar el cursor y la conexión
        self.cur.close()
        self.conn.close()

    def consultarEventos(self):
        consulta = 'SELECT * FROM eventos'
        self.cur.execute(consulta)
        # Obtener todas las filas y guardarlas en una lista de diccionarios
        filas = self.cur.fetchall()
        columnas = [desc[0] for desc in self.cur.description]

        eventos = []
        for fila in filas:
            evento = dict(zip(columnas, fila))
            eventos.append(evento)
        
        return eventos

    def consultarUsuarios(self):
        consulta = 'SELECT * FROM usuarios'
        self.cur.execute(consulta)
        # Obtener todas las filas y guardarlas en una lista de diccionarios
        filas = self.cur.fetchall()
        columnas = [desc[0] for desc in self.cur.description]

        usuarios = []
        for fila in filas:
            usuario = dict(zip(columnas, fila))
            usuarios.append(usuario)
        
        return usuarios
    
    def isExist(self, tabla, col, datos):
        consulta = f'SELECT COUNT(*) FROM {tabla} WHERE {col}{tabla[:-1]} = %s'
        self.cur.execute(consulta, (datos,))
        resultado = self.cur.fetchone()[0]
        return resultado > 0
    
    def consultarTipoU(self, correo):
        consulta = 'SELECT tipousuario FROM usuarios WHERE correousuario = %s'
        self.cur.execute(consulta, (correo,))
        resultado=self.cur.fetchone()[0]
        return resultado

    def registarUsuario(self, nombre,tipocc,cedula,apellido,correo,contra):
        
        consulta = '''INSERT INTO usuarios (idusuario,tipoid,tipousuario,nomusuario,apeusuario,correousuario,contrausuario) 
              VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        datos=(cedula,tipocc,3,nombre.capitalize(),apellido.capitalize(),correo.lower(),contra)
        self.cur.execute(consulta,datos)
        self.conn.commit()
        
    def llenar_base_datos_usuario(self):
        self.crear_tabla_usuarios()
        self.cargar_usuarios()
        self.obtener_usuarios()
        
    def cargar_usuarios(self):
        '''Este metodo carga la tabla usuarios del script Usuarios.csv'''
        ruta = self.dir_simes + '\\script_db_Simes\\Usuarios.csv'
        datos = f'''copy usuarios(nomusuario,apelliusuario,ccusuario,correo,contrasena) from '{ruta}'
        with (delimiter '|',header,encoding'UTF-8',format'csv' )'''
        self.cur.execute(datos)
        print('parece que se llenaron los datos')
        self.cur.execute('select nomusuario from usuarios')
        datos = self.cur.fetchall()
        for i in datos:
            print(i)
        print(type(datos))

    def crear_tabla_usuarios(self):
        '''Este metodo elimina en el caso de que se haya creado una tabla antes 
        y vuelve a crear la tabla Usuarios'''
        ruta = self.dir_simes + '\\script_db_Simes\\tabla_usuarios.sql'
        with open(ruta,"r") as tabla:
            lectura = tabla.read()
        self.cur.execute("drop table usuarios")
        self.cur.execute(lectura)
    
    def obtener_usuarios(self):
        self.cur.execute("select * from usuarios")
        lista = self.cur.fetchall()
        for i in lista :
            print(i)
            
    def escribir_usuario(self,nombre, apellido, cedula, correo, contraseña, foto = None):
        '''Este metodo permite añadir un usuario a la ves, los parametro que se
        deben pasar al metodo son nombre, apellido, cedula, correo y contraseña,
        la ruta de la foto es opcional'''
        # PRIMERO SE AÑADE EL NUEVO USUARIO A LA BASE DE DATOS 
        us = f"insert into usuarios (nomusuario,apelliusuario,ccusuario,correo,contrasena,foto) values ('{nombre}','{apellido}','{cedula}','{correo}','{contraseña}','{foto}')"
        self.cur.execute(us)
        self.obtener_usuarios()
        # AHORA SE AÑADE EL USUARIO A EL SCRIPT PARA QUE APAREZCA EN LA BASE DE DATOS
        us = f"\n{nombre}|{apellido}|{cedula}|{correo}|{contraseña}|{foto}"
        ruta_us = self.dir_simes + '\\script_db_Simes\\Usuarios.csv'
        with open(ruta_us,'a') as escribir:
            escribir.write(us)