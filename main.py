import sqlite3
import hashlib

def conectar_db():
    conexion = sqlite3.connect("gym_pro.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion

def inicializar_roles():
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    roles_por_defecto = [("Socio",), ("Administrador",), ("Recepcionista",)]
    
    cursor.executemany("INSERT OR IGNORE INTO Rol (nombre) VALUES (?)", roles_por_defecto)
    
    conexion.commit()
    conexion.close()
    
class Usuario:
    def __init__(self, id_rol, documento, nombre, clave):
        self.id_rol = id_rol
        self.documento = documento
        self.nombre = nombre
        self.clave_hash = self._encriptar_clave(clave)
    
    def _encriptar_clave(self, clave):
        return hashlib.sha256(clave.encode()).hexdigest()
    
    def registrar(self):
        
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO Usuario (id_rol, documento, nombre, clave_hash) VALUES (?,?,?,?)",
                (self.id_rol, self.documento, self.nombre, self.clave_hash)
            )
            conexion.commit()
            print(f"Exito: Usuario '{self.nombre}' registrado correctamente.")
            
        except sqlite3.IntegrityError:
            print(f"Error: El documento '{self.documento}' ya esta registrado.")
            
        finally:
            conexion.close()
            
    @staticmethod
    def autenticar(documento, clave):
        
        clave_hash = hashlib.sha256(clave.encode()).hexdigest()
        
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        cursor.execute(
            "SELECT id_usuario, nombre, id_rol FROM Usuario WHERE documento = ? AND clave_hash = ?",
            (documento, clave_hash)
        )
        
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado:
            print(f"Acceso concedido. Bienvenido, {resultado[1]}.")
            return resultado 
        else:
            print("Acceso denegado. Documento o contraseña incorrectos.")
            return None
        
if __name__ == "__main__":
    inicializar_roles()
    
    print("--- Registrando al socio Principal ---")
    socio_dueño = Usuario(id_rol=1, documento="123456789", nombre="Miguel Gomez", clave="admin123")
    socio_dueño.registrar()
    
    print("\n--- Probando Login ---")
    Usuario.autenticar("123456789", "admin123")
    Usuario.autenticar("123456789", "clavefalsa")
            
