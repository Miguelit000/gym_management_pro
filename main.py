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

class Plan:
    def __init__(self, nombre, dias_duracion, precio_base, id_plan=None):
        self.id_plan = id_plan
        self.nombre = nombre
        self.dias_duracion = dias_duracion
        self.precio_base = precio_base
        
    def registrar(self):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO Plan (nombre, dias_duracion, precio_base) VALUES (?,?,?)",
                (self.nombre, self.dias_duracion, self.precio_base)
            )
            conexion.commit()
            print(f"Plan '{self.nombre}' (Duracion: {self.dias_duracion} dias) creado correctamente.")
        except Exception as e:
            print(f"Error al crear el plan: {e}")
        finally:
            conexion.close()
            
class Cliente:
    def __init__(self, documento, nombre, telefono, email, id_cliente=None):
        self.id_cliente = id_cliente
        self.documento = documento
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
    
    def registrar(self):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO Cliente (documento, nombre, telefono, email) VALUES (?,?,?,?)",
                (self.documento, self.nombre, self.telefono, self.email)
            )
            conexion.commit()
            print(f"Cliente '{self.nombre}' registrado correctamente.")
        except sqlite3.IntegrityError:
            print(f"Error: El cliente con documento '{self.documento}' ya exite en el sistema.")
        finally:
            conexion.close()
            
    @staticmethod
    def buscar_por_documento(documento):
        
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Cliente WHERE documento = ?", (documento,))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado:
            return resultado
        else:
            print(f"Cliente con documento {documento} no encontrado.")
            return None
        
if __name__ == "__main__":
    inicializar_roles()
    
    print("--- Registrando al socio Principal ---")
    socio_dueño = Usuario(id_rol=1, documento="123456789", nombre="Miguel Gomez", clave="admin123")
    socio_dueño.registrar()
    
    print("\n--- Creando Planes del Gimnasio ---")
    plan_mensual = Plan(nombre="Mensualidad Estandar", dias_duracion=30, precio_base=80000)
    plan_anual = Plan(nombre="Plan Anual VIP", dias_duracion=365, precio_base=800000)
    
    plan_mensual.registrar()
    plan_anual.registrar()
    
    print("\n--- Registrando Clientes ---")
    cliente_uno = Cliente(documento="987654321", nombre="Ana Martinez", telefono="3001234567", email="ana@gmail.com")
    cliente_uno.registrar()
    
    cliente_duplicado = Cliente(documento="987654321", nombre="Ana Falsa", telefono="000", email="fake")
    cliente_duplicado.registrar()
    
    datos_ana = Cliente.buscar_por_documento("987654321")
    if datos_ana:
        print(f"Datos encontrados: {datos_ana}")
        
   
            
