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
            
class Asistencia:
    @staticmethod
    def registrar_entrada(documento):
        
        cliente = Cliente.buscar_por_documento(documento)
        
        if not cliente:
            print("\n" + "="*50)
            print("ALERTA: Tarjeta o documento no reconocido")
            print("="*50 + "\n")
            return
        
        id_cliente = cliente[0]
        
        estado_mensaje = Membresia.verificar_estado(documento)
        
        estado_bd = "Denegado"
        if "🟢" in estado_mensaje:
            estado_bd = "Permitido"
        elif "🟡" in estado_mensaje:
            estado_bd = "Gracia"
            
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Asistencia (
                    id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER,
                    fecha_hora DATETIME CURRENT_TIMESTAMP,
                    estado_acceso TEXT,
                    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
                    )
                ''')
            
        try:
            cursor.execute(
                "INSERT INTO Asistencia (id_cliente, estado_acceso) VALUES (?,?)",
                (id_cliente, estado_bd)
            )
            
            conexion.commit()
            
            print("\n" + "="*50)
            print(estado_mensaje)
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"Error al guardar el registro de asistencia: {e}")
        finally:
            conexion.close()
            
class Producto:
    def __init__(self, codigo, nombre, precio_venta, stock, id_producto=None):
        self.id_producto = id_producto
        self.codigo = codigo
        self.nombre = nombre
        self.precio_venta = precio_venta
        self.stock = stock
        
    def registrar(self):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO Producto (codigo, nombre, precio_venta, stock) VALUES (?,?,?,?)",
                (self.codigo, self.nombre, self.precio_venta, self.stock)
            )
            conexion.commit()
            print(f"Producto registrado: {self.nombre} (Stock inicial: {self.stock})")
        except sqlite3.IntegrityError:
            print(f"Error: El codigo de producto '{self.codigo}' ya existe.")
        finally:
            conexion.close()
            
    @staticmethod
    def vender(codigo_producto, cantidad, id_usuario_vendedor):
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        try:
            cursor.execute("SELECT id_producto, nombre, precio_venta, stock FROM Producto WHERE codigo = ?", (codigo_producto,))
            producto = cursor.fetchone()
            
            if not producto:
                print(f"Error: Producto con codigo '{codigo_producto}' no encontrado.")
                return
            
            id_prod, nombre, precio, stock_actual = producto
            
            if stock_actual < cantidad:
                print(f"Alerta de Inventario: No hay suficientes stock de '{nombre}'. Disponible: {stock_actual}.")
                return
            
            total_venta = precio * cantidad
            nuevo_stock = stock_actual - cantidad
            
            cursor.execute("UPDATE Producto SET stock = ? WHERE id_producto = ?", (nuevo_stock, id_prod))
            
            descripcion_venta = f"Venta POS: {cantidad}x {nombre}"
            
            cursor.execute(
                "INSERT INTO Transaccion (id_usuario, tipo, monto, descripcion) VALUES (?, 'Ingreso', ?,?)",
                (id_usuario_vendedor, total_venta, descripcion_venta)
            )
            
            conexion.commit()
            print(f"Venta exitosa: {cantidad}x {nombre}. Total: ${total_venta:,.2f}. (Stock restante: {nuevo_stock})")
        
        except Exception as e:
            conexion.rollback()
            print(f"Error critico en la venta: {e}")
        finally:
            conexion.close()
            
            
            
                
            
        
                
        
## --- 9. ZONA DE PRUEBAS (SIMULADOR DE TIENDA) ---
if __name__ == "__main__":
    print("\n--- FASE 4: INVENTARIO Y PUNTO DE VENTA ---")
    
    # 1. Surtimos el inventario (Llega el pedido del proveedor)
    print("\n📦 Registrando productos en el sistema...")
    agua = Producto(codigo="A001", nombre="Botella de Agua 600ml", precio_venta=3000, stock=50)
    proteina = Producto(codigo="P001", nombre="Proteína Whey Scoop", precio_venta=8000, stock=20)
    
    agua.registrar()
    proteina.registrar()

    # 2. Simulamos ventas en recepción
    print("\n🛒 Simulando ventas...")
    # Miguel (id_usuario=1) vende 2 botellas de agua
    Producto.vender(codigo_producto="A001", cantidad=2, id_usuario_vendedor=1)
    
    # Miguel vende 1 scoop de proteína
    Producto.vender(codigo_producto="P001", cantidad=1, id_usuario_vendedor=1)
    
    # 3. Forzamos un error de stock para probar la seguridad
    print("\n⚠️ Intentando vender más de lo que hay...")
    Producto.vender(codigo_producto="P001", cantidad=25, id_usuario_vendedor=1)