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
        
class  Transaccion:
    def __init__(self, id_usuario, tipo, monto, descripcion):
        self.id_usuario = id_usuario
        self.tipo = tipo
        self.monto = monto
        self.descripcion = descripcion
        
    def registrar(self):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO Transaccion (id_usuario, tipo, monto, descripcion) VALUES (?,?,?,?)",
                (self.id_usuario, self.tipo, self.monto, self.descripcion)
            )
            conexion.commit()
            id_tx = cursor.lastrowid
            print(f"Transaccion #{id_tx} registrada: {self.tipo} por ${self.monto:,.2f}. (Cajero ID: {self.id_usuario})")
            return id_tx
        except Exception as e:
            print(f"Error al registrar transaccion: {e}")
        finally:
            conexion.close()
            
    @staticmethod
    def anular(id_transaccion_original, id_usuario_anula, motivo):
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        try:
            cursor.execute("SELECT monto, descripcion FROM Transaccion WHERE id_transaccion = ?", (id_transaccion_original,))
            original = cursor.fetchone()
            
            if not original:
                print("Error: La transaccion original no existe.")
                return
            
            monto_original, desc_original = original
            
            monto_anulacion = -monto_original
            desc_anulacion = f"ANULACION de Tx #{id_transaccion_original}: {motivo}"
            
            cursor.execute(
                "INSERT INTO Transaccion (id_usuario, tipo, monto, descripcion) VALUES (?, 'Anulacion', ?,?)",
                (id_usuario_anula, monto_anulacion, desc_anulacion)
            )
            nueva_tx_id = cursor.lastrowid
            
            cursor.execute(
                "INSERT INTO Auditoria (id_usuario, accion, tabla_afectada, registro_id, valor_anterior, valor_nuevo) VALUES (?,?,?,?,?,?)",
                (id_usuario_anula, "ANULAR_TRANSACCION", "Transaccion", id_transaccion_original, str(monto_original), str(monto_anulacion))
            )
            
            conexion.commit()
            print(f"¡ALERTA! Transaccion #{id_transaccion_original} fue ANULADA. Se genero la Tx #{nueva_tx_id} por ${monto_anulacion:,.2f}")
        except Exception as e:
            conexion.rollback()
            print(f"Error critico en la anulacion: {e}")
        finally:
            conexion.close()
            
        
                
        
if __name__ == "__main__":
    # Suponemos que Miguel (id_usuario = 1) ya está en la base de datos por las pruebas anteriores
    
    print("\n--- FASE 2: BLINDAJE FINANCIERO ---")
    
    print("\n1. Registrando el pago de una mensualidad (Ingreso)")
    # Miguel cobra $80,000 por la mensualidad de Ana
    tx_ingreso = Transaccion(id_usuario=1, tipo="Ingreso", monto=80000, descripcion="Pago Mensualidad - Ana Martinez")
    id_transaccion_cobro = tx_ingreso.registrar()

    print("\n2. Registrando un pago de la luz (Gasto)")
    # Miguel paga los servicios del gimnasio
    tx_gasto = Transaccion(id_usuario=1, tipo="Gasto", monto=-150000, descripcion="Pago de Energía Eléctrica")
    tx_gasto.registrar()

    print("\n3. ¡ERROR! Simulando la anulación de un pago...")
    # Resulta que el pago de Ana fue con un billete falso, Miguel tiene que anularlo.
    # No usamos DELETE, usamos nuestro sistema seguro:
    Transaccion.anular(id_transaccion_original=id_transaccion_cobro, id_usuario_anula=1, motivo="Cliente entregó billete falso")
        
   
            
