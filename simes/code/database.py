#importacion del modulo
import psycopg2
class DataBase():
    def __init__(self) -> None:
        # Conexion a base de datos
        print('esto si se ejecuta')
        self.conn = psycopg2.connect(user='postgres', password = 'POSTGRES1',host='127.0.0.1', port='5432', database='db_Simes')
        # Utilizar cursor
        self.cur = self.conn.cursor()

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

