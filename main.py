import sqlite3
import hashlib
from datetime import datetime, timedelta, date

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
        
class Membresia:
    def __init__(self, id_cliente, id_plan, fecha_inicio, fecha_fin, id_membresia=None):
        self.id_membresia = id_membresia
        self.id_cliente = id_cliente
        self.id_plan = id_plan
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        
    def registrar(self):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO Membresia (id_cliente, id_plan, fecha_inicio, fecha_fin) VALUES (?,?,?,?)",
                (self.id_cliente, self.id_plan, str(self.fecha_inicio), str(self.fecha_fin))
            )
            conexion.commit()
            print(f"Membresia registrada: Del {self.fecha_inicio} al {self.fecha_fin}.")
        except Exception as e:
            print(f"Error al registrar memebresia: {e}")
        finally:
            conexion.close()
    
    @staticmethod
    def crear_nueva(id_cliente, id_plan, dias_duracion):
        fecha_inicio = date.today()
        fecha_fin = fecha_inicio + timedelta(days=dias_duracion)
        
        nueva_membresia = Membresia(id_cliente, id_plan, fecha_inicio, fecha_fin)
        nueva_membresia.registrar()
        return nueva_membresia
    
    @staticmethod
    def verificar_estado(documento_cliente):
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        cursor.execute('''
                SELECT m.fecha_fin, c.nombre
                FROM Membresia m
                JOIN Cliente c ON m.id_cliente = c.id_cliente
                WHERE c.documento = ?
                ORDER BY m.fecha_fin DESC LIMIT 1
        ''', (documento_cliente,))
        
        resultado = cursor.fetchone()
        conexion.close()
        
        if not resultado:
            return "Bloqueado: Cliente no tiene membresias registradas."
        
        fecha_fin_str, nombre_cliente = resultado
        
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        hoy = date.today()
        
        dias_restantes = (fecha_fin - hoy).days
        
        if dias_restantes >= 0:
            return F"Acceso Permitido: {nombre_cliente}. Plan vigente ({dias_restantes} dias restantes)."
        elif dias_restantes >= 3:
            dias_vencidos = abs(dias_restantes)
            return f"Acceso en gracia: {nombre_cliente}. Vencio hace {dias_vencidos} dia(s). Recuerda pagar en recepcion."
        else:
            return f"Acceso Denegado: {nombre_cliente}. Plan vencido hace {abs(dias_restantes)} dias."
        
        
                
        
if __name__ == "__main__":
    inicializar_roles()
    
    print("\n--- Vendiendo una Membresía a Ana ---")
    # Ana compra el plan mensual (id_plan=1, dura 30 días). Ana es id_cliente=1.
    Membresia.crear_nueva(id_cliente=1, id_plan=1, dias_duracion=30)
    
    print("\n--- Verificando Acceso en la Puerta ---")
    # Simulamos que Ana pasa la tarjeta por el lector hoy
    estado_ana = Membresia.verificar_estado("987654321")
    print(estado_ana)

    # --- SIMULACIÓN DE PERIODO DE GRACIA ---
    # Vamos a forzar una membresía vieja directamente en la BD para probar el semáforo amarillo
    print("\n--- Simulando cliente en periodo de gracia (Venció hace 2 días) ---")
    conexion = conectar_db()
    cursor = conexion.cursor()
    # Registramos un cliente de prueba
    cursor.execute("INSERT OR IGNORE INTO Cliente (documento, nombre) VALUES ('111', 'Pedro Prueba')")
    id_pedro = cursor.lastrowid if cursor.lastrowid else 2 
    
    # Le creamos una membresía que venció hace exactamente 2 días
    fecha_vieja = (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO Membresia (id_cliente, id_plan, fecha_inicio, fecha_fin) VALUES (?, 1, '2026-01-01', ?)", (id_pedro, fecha_vieja))
    conexion.commit()
    conexion.close()

    estado_pedro = Membresia.verificar_estado("111")
    print(estado_pedro)
        
   
            
