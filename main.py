"""
=============================================================================
Gym Management Pro - Backend (main.py)
Autor: Miguelit000
Descripción: Este archivo contiene toda la lógica de negocio y la conexión 
a la base de datos SQLite. Gestiona usuarios, clientes, planes, inventario, 
membresías, accesos y la contabilidad del gimnasio.
=============================================================================
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta, date

# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS
# ==========================================
def conectar_db():
    """Establece la conexión con la base de datos y activa las llaves foráneas para seguridad."""
    conexion = sqlite3.connect("gym_pro.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion

def inicializar_roles():
    """Crea los roles básicos del sistema si aún no existen."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    roles_por_defecto = [("Socio",), ("Administrador",), ("Recepcionista",)]
    cursor.executemany("INSERT OR IGNORE INTO Rol (nombre) VALUES (?)", roles_por_defecto)
    conexion.commit()
    conexion.close()

# ==========================================
# MÓDULO 1: GESTIÓN DE EQUIPO (USUARIOS)
# ==========================================
class Usuario:
    """Maneja a los empleados del sistema (Administradores y Recepcionistas)."""
    
    def __init__(self, id_rol, documento, nombre, clave):
        self.id_rol = id_rol
        self.documento = documento
        self.nombre = nombre
        self.clave_hash = self._encriptar_clave(clave)
    
    def _encriptar_clave(self, clave):
        """Convierte la contraseña en un código seguro e irreversible (Hash)."""
        return hashlib.sha256(clave.encode()).hexdigest()
    
    def registrar(self):
        """Guarda un nuevo empleado en la base de datos."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO Usuario (id_rol, documento, nombre, clave_hash) VALUES (?,?,?,?)",
                (self.id_rol, self.documento, self.nombre, self.clave_hash)
            )
            conexion.commit()
            return True, f"Éxito: Usuario '{self.nombre}' registrado correctamente."
        except sqlite3.IntegrityError:
            return False, f"Error: El documento '{self.documento}' ya está registrado."
        finally:
            conexion.close()

    @staticmethod
    def obtener_todos():
        """Obtiene la lista de empleados para mostrar en la tabla visual."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            # Traduce el número de rol a texto (Admin/Recepcionista)
            cursor.execute("""
                SELECT documento, nombre, 
                       CASE WHEN id_rol = 2 THEN 'Administrador' ELSE 'Recepcionista' END as rol 
                FROM Usuario
            """)
            return True, cursor.fetchall()
        except Exception as e:
            return False, f"Error al cargar usuarios: {e}"
        finally:
            conexion.close()

    @staticmethod
    def actualizar(documento, nombre, id_rol, clave_nueva=""):
        """Modifica los datos de un empleado. Actualiza la clave solo si se escribe una nueva."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            if clave_nueva != "":
                import hashlib
                clave_hash = hashlib.sha256(clave_nueva.encode()).hexdigest()
                cursor.execute(
                    "UPDATE Usuario SET nombre = ?, id_rol = ?, clave_hash = ? WHERE documento = ?",
                    (nombre, id_rol, clave_hash, documento)
                )
            else:
                cursor.execute(
                    "UPDATE Usuario SET nombre = ?, id_rol = ? WHERE documento = ?",
                    (nombre, id_rol, documento)
                )
            conexion.commit()
            return True, "Datos del usuario actualizados correctamente."
        except Exception as e:
            return False, f"Error al actualizar: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar(documento):
        """Borra un empleado permanentemente si no tiene transacciones asociadas."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Usuario WHERE documento = ?", (documento,))
            conexion.commit()
            return True, "Usuario eliminado permanentemente del sistema."
        except sqlite3.IntegrityError:
            return False, "No se puede eliminar porque este usuario ya ha procesado ventas o gastos."
        except Exception as e:
            return False, f"Error al eliminar: {e}"
        finally:
            conexion.close()
            
    @staticmethod
    def autenticar(documento, clave):
        """Verifica las credenciales para el inicio de sesión y permisos especiales."""
        import hashlib
        clave_hash = hashlib.sha256(clave.encode()).hexdigest()
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, id_rol, nombre FROM Usuario WHERE documento = ? AND clave_hash = ?", (documento, clave_hash))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario 

# ==========================================
# MÓDULO 2: CATÁLOGO DE PLANES
# ==========================================
class Plan:
    """Maneja el catálogo de planes que el gimnasio ofrece (Mensual, Anual, etc.)."""
    
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
            return True, f"Plan '{self.nombre}' creado exitosamente."
        except Exception as e:
            return False, f"Error al registrar el plan: {e}"
        finally:
            conexion.close()

    @staticmethod
    def obtener_todos():
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_plan, nombre, dias_duracion, precio_base FROM Plan")
            return True, cursor.fetchall()
        except Exception as e:
            return False, f"Error al cargar planes: {e}"
        finally:
            conexion.close()

    @staticmethod
    def actualizar(id_plan, nombre, dias_duracion, precio_base):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE Plan SET nombre = ?, dias_duracion = ?, precio_base = ? WHERE id_plan = ?",
                (nombre, dias_duracion, precio_base, id_plan)
            )
            conexion.commit()
            return True, "Precio y datos del plan actualizados correctamente."
        except Exception as e:
            return False, f"Error al actualizar: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_plan):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Plan WHERE id_plan = ?", (id_plan,))
            conexion.commit()
            return True, "Plan eliminado del sistema."
        except sqlite3.IntegrityError:
            return False, "Bloqueo: No puedes borrar este plan porque hay clientes que lo tienen activo en este momento."
        except Exception as e:
            return False, f"Error al eliminar: {e}"
        finally:
            conexion.close()

# ==========================================
# MÓDULO 3: GESTIÓN DE CLIENTES
# ==========================================
class Cliente:
    """Maneja los datos personales de las personas inscritas en el gimnasio."""
    
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
            return True, f"Cliente '{self.nombre}' registrado correctamente."
        except sqlite3.IntegrityError:
            return False, f"Error: El cliente con documento '{self.documento}' ya existe en el sistema."
        except Exception as e:
            return False, f"Error inesperado: {e}"
        finally:
            conexion.close()
            
    @staticmethod
    def buscar_por_documento(documento):
        """Busca un cliente específico por su ID. Útil para vender membresías o puerta."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Cliente WHERE documento = ?", (documento,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado
        
    @staticmethod
    def obtener_todos():
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT documento, nombre, telefono, email FROM Cliente")
            return True, cursor.fetchall()
        except Exception as e:
            return False, f"Error al cargar clientes: {e}"
        finally:
            conexion.close()

    @staticmethod
    def actualizar(documento, nombre, telefono, email):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE Cliente SET nombre = ?, telefono = ?, email = ? WHERE documento = ?",
                (nombre, telefono, email, documento)
            )
            conexion.commit()
            return True, "Datos del cliente actualizados correctamente."
        except Exception as e:
            return False, f"Error al actualizar: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar(documento):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Cliente WHERE documento = ?", (documento,))
            conexion.commit()
            return True, "Cliente eliminado del sistema."
        except sqlite3.IntegrityError:
            return False, "Bloqueo de Seguridad: No puedes eliminar a este cliente porque tiene un historial de membresías o asistencias guardado."
        except Exception as e:
            return False, f"Error al eliminar: {e}"
        finally:
            conexion.close()

# ==========================================
# MÓDULO 4: ASIGNACIÓN DE MEMBRESÍAS
# ==========================================
class Membresia:
    """Controla los planes que han sido vendidos a los clientes y sus fechas de vencimiento."""
    
    def __init__(self, id_cliente, id_plan, fecha_inicio, fecha_fin, id_membresia=None):
        self.id_membresia = id_membresia
        self.id_cliente = id_cliente
        self.id_plan = id_plan
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        
    def registrar(self):
        """Guarda la membresía calculada en la base de datos."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO Membresia (id_cliente, id_plan, fecha_inicio, fecha_fin) VALUES (?,?,?,?)",
                (self.id_cliente, self.id_plan, str(self.fecha_inicio), str(self.fecha_fin))
            )
            conexion.commit()
            return True, f"Membresía registrada: Del {self.fecha_inicio} al {self.fecha_fin}."
        except Exception as e:
            return False, f"Error al registrar membresía: {e}"
        finally:
            conexion.close()
    
    @staticmethod
    def crear_nueva(id_cliente, id_plan, dias_duracion):
        """Calcula la fecha de vencimiento sumando los días al día de hoy."""
        fecha_inicio = date.today()
        fecha_fin = fecha_inicio + timedelta(days=dias_duracion)
        nueva_membresia = Membresia(id_cliente, id_plan, fecha_inicio, fecha_fin)
        exito, mensaje = nueva_membresia.registrar()
        return exito, mensaje
    
    @staticmethod
    def verificar_estado(documento_cliente):
        """Lógica principal de la Puerta: Verifica si el cliente puede pasar."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Trae la membresía más reciente del cliente
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
        
        # Cálculo de días restantes
        dias_restantes = (fecha_fin - hoy).days
        
        # Semáforo de acceso
        if dias_restantes >= 0:
            return f"Acceso Permitido: {nombre_cliente}. Plan vigente ({dias_restantes} dias restantes)."
        elif dias_restantes >= -3: # PERÍODO DE GRACIA (Hasta 3 días vencido)
            dias_vencidos = abs(dias_restantes)
            return f"Acceso en gracia: {nombre_cliente}. Vencio hace {dias_vencidos} dia(s). Recuerda pagar en recepcion."
        else:
            return f"Acceso Denegado: {nombre_cliente}. Plan vencido hace {abs(dias_restantes)} dias."
    
    @staticmethod
    def obtener_todas():
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            # JOIN para traer textos en lugar de IDs (Nombres y Planes)
            cursor.execute('''
                SELECT m.id_membresia, c.documento, c.nombre, p.nombre, m.fecha_fin
                FROM Membresia m
                JOIN Cliente c ON m.id_cliente = c.id_cliente
                JOIN Plan p ON m.id_plan = p.id_plan
                ORDER BY m.id_membresia DESC
            ''')
            return True, cursor.fetchall()
        except Exception as e:
            return False, f"Error al cargar membresías: {e}"
        finally:
            conexion.close()

    @staticmethod
    def actualizar(id_membresia, id_plan, dias_duracion):
        """Recalcula el vencimiento basado en la nueva duración asignada."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT fecha_inicio FROM Membresia WHERE id_membresia = ?", (id_membresia,))
            resultado = cursor.fetchone()
            if not resultado:
                return False, "Membresía no encontrada."
                
            fecha_inicio_str = resultado[0]
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            nueva_fecha_fin = fecha_inicio + timedelta(days=dias_duracion)

            cursor.execute(
                "UPDATE Membresia SET id_plan = ?, fecha_fin = ? WHERE id_membresia = ?", 
                (id_plan, str(nueva_fecha_fin), id_membresia)
            )
            conexion.commit()
            return True, f"Membresía actualizada. Nuevo vencimiento: {nueva_fecha_fin}"
        except Exception as e:
            return False, f"Error al actualizar: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_membresia):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Membresia WHERE id_membresia = ?", (id_membresia,))
            conexion.commit()
            return True, "Registro de membresía eliminado."
        except Exception as e:
            return False, f"Error al eliminar: {e}"
        finally:
            conexion.close()

# ==========================================
# MÓDULO 5: CONTABILIDAD Y AUDITORÍA
# ==========================================
class Transaccion:
    """Libro contable del sistema. Registra cualquier movimiento de dinero."""
    
    def __init__(self, id_usuario, tipo, monto, descripcion):
        self.id_usuario = id_usuario
        self.tipo = tipo # "Ingreso", "Gasto" o "Anulacion"
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
            return id_tx
        except Exception as e:
            print(f"Error al registrar transaccion: {e}")
        finally:
            conexion.close()
            
    @staticmethod
    def anular(id_transaccion_original, id_usuario_anula, motivo):
        """Genera una contra-transacción para cuadrar caja sin borrar el historial original."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT monto, descripcion FROM Transaccion WHERE id_transaccion = ?", (id_transaccion_original,))
            original = cursor.fetchone()
            if not original:
                return
            
            monto_original, desc_original = original
            monto_anulacion = -monto_original
            desc_anulacion = f"ANULACION de Tx #{id_transaccion_original}: {motivo}"
            
            cursor.execute(
                "INSERT INTO Transaccion (id_usuario, tipo, monto, descripcion) VALUES (?, 'Anulacion', ?,?)",
                (id_usuario_anula, monto_anulacion, desc_anulacion)
            )
            conexion.commit()
        except Exception as e:
            conexion.rollback()
        finally:
            conexion.close()

# ==========================================
# MÓDULO 6: CONTROL DE ACCESO
# ==========================================
class Asistencia:
    """Guarda el historial de las veces que los clientes cruzan la puerta."""
    
    @staticmethod
    def registrar_entrada(documento):
        """Verifica la membresía y guarda el registro de la visita."""
        cliente = Cliente.buscar_por_documento(documento)
        if not cliente:
            return False, "ALERTA: Tarjeta o documento no reconocido en el sistema."
        
        id_cliente = cliente[0]
        estado_mensaje = Membresia.verificar_estado(documento)
        
        estado_bd = "Denegado"
        acceso_concedido = False
        
        if "Acceso Permitido" in estado_mensaje:
            estado_bd = "Permitido"
            acceso_concedido = True
        elif "Acceso en gracia" in estado_mensaje:
            estado_bd = "Gracia"
            acceso_concedido = True
            
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Crea la tabla si por alguna razón no se había creado en el script principal
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Asistencia (
                    id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER,
                    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                    estado_acceso TEXT,
                    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
                    )
                ''')
        try:
            cursor.execute("INSERT INTO Asistencia (id_cliente, estado_acceso) VALUES (?,?)", (id_cliente, estado_bd))
            conexion.commit()
            return acceso_concedido, estado_mensaje
        except Exception as e:
            return False, f"Error al guardar el registro de asistencia: {e}"
        finally:
            conexion.close()

# ==========================================
# MÓDULO 7: INVENTARIO Y PUNTO DE VENTA
# ==========================================
class Producto:
    """Maneja los artículos físicos que se venden en el gimnasio."""
    
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
            return True, f"Producto registrado: {self.nombre} (Stock inicial: {self.stock})"
        except sqlite3.IntegrityError:
            return False, f"Error: El código de producto '{self.codigo}' ya existe."
        finally:
            conexion.close()
            
    @staticmethod
    def vender(codigo_producto, cantidad, id_usuario_vendedor):
        """Descuenta del inventario y registra el dinero en las transacciones (Punto de Venta)."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        try:
            cursor.execute("SELECT id_producto, nombre, precio_venta, stock FROM Producto WHERE codigo = ?", (codigo_producto,))
            producto = cursor.fetchone()
            
            if not producto:
                return False, f"Producto con código '{codigo_producto}' no encontrado."
            
            id_prod, nombre, precio, stock_actual = producto
            
            # Validación de stock
            if stock_actual < cantidad:
                return False, f"Alerta de Inventario: No hay suficiente stock de '{nombre}'. Disponible: {stock_actual}."
            
            total_venta = precio * cantidad
            nuevo_stock = stock_actual - cantidad
            
            # 1. Restar el inventario
            cursor.execute("UPDATE Producto SET stock = ? WHERE id_producto = ?", (nuevo_stock, id_prod))
            
            # 2. Sumar el dinero a la caja
            descripcion_venta = f"Venta POS: {cantidad}x {nombre}"
            cursor.execute(
                "INSERT INTO Transaccion (id_usuario, tipo, monto, descripcion) VALUES (?, 'Ingreso', ?,?)",
                (id_usuario_vendedor, total_venta, descripcion_venta)
            )
            
            conexion.commit()
            return True, f"Venta exitosa: {cantidad}x {nombre}\nTotal: ${total_venta:,.2f}\n(Stock restante: {nuevo_stock})"
        
        except Exception as e:
            conexion.rollback() # Si algo falla, deshace la venta y el descuento de stock
            return False, f"Error crítico en la venta: {e}"
        finally:
            conexion.close()
            
    @staticmethod
    def obtener_todos():
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT codigo, nombre, precio_venta, stock FROM Producto")
            productos = cursor.fetchall()
            return True, productos
        except Exception as e:
            return False, f"Error al cargar productos: {e}"
        finally:
            conexion.close()
        
    @staticmethod
    def actualizar(codigo, nombre, precio_venta, stock):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE Producto SET nombre = ?, precio_venta = ?, stock = ? WHERE codigo = ?",
                (nombre, precio_venta, stock, codigo)
            )
            conexion.commit()
            return True, "Datos del producto actualizados correctamente."
        except Exception as e:
            return False, f"Error al actualizar el producto: {e}"
        finally:
            conexion.close()

    @staticmethod
    def eliminar(codigo):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Producto WHERE codigo = ?", (codigo,))
            conexion.commit()
            return True, "Producto eliminado del inventario."
        except sqlite3.IntegrityError:
            return False, "Bloqueo: No puedes eliminar este producto porque ya está registrado en el historial de ventas."
        except Exception as e:
            return False, f"Error al eliminar: {e}"
        finally:
            conexion.close()

# ==========================================
# MÓDULO 8: ESTADÍSTICAS FINANCIERAS
# ==========================================
class Dashboard:
    """Genera la información financiera consolidada para el panel de Reportes."""
    
    @staticmethod
    def generar_reporte_financiero(periodo=None):
        """Calcula los totales de ingresos, gastos y utilidad aplicando filtros de tiempo."""
        from datetime import datetime
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        total_ingresos = total_gastos = total_anulaciones = 0.0
        
        try: 
            # Filtro por período (Mes/Año o Histórico completo)
            if periodo == "TODO":
                filtro = ""
                parametros = ()
            else:
                if not periodo:
                    periodo = datetime.now().strftime('%Y-%m')
                # Filtramos las transacciones usando LIKE para buscar por el mes indicado
                filtro = " AND fecha LIKE ?" 
                parametros = (f"{periodo}%",)

            # Sumatoria de Ingresos
            cursor.execute(f"SELECT COALESCE(SUM(monto), 0) FROM Transaccion WHERE tipo = 'Ingreso'{filtro}", parametros)
            fila = cursor.fetchone()
            if fila: total_ingresos = fila[0]
            
            # Sumatoria de Gastos (Negativos)
            cursor.execute(f"SELECT COALESCE(SUM(monto), 0) FROM Transaccion WHERE tipo = 'Gasto'{filtro}", parametros)
            fila = cursor.fetchone()
            if fila: total_gastos = fila[0]
            
            # Sumatoria de Anulaciones
            cursor.execute(f"SELECT COALESCE(SUM(monto), 0) FROM Transaccion WHERE tipo = 'Anulacion'{filtro}", parametros)
            fila = cursor.fetchone()
            if fila: total_anulaciones = fila[0]
            
            utilidad_neta = total_ingresos + total_gastos + total_anulaciones
            
            datos = {
                "ingresos": total_ingresos,
                "gastos": total_gastos,
                "anulaciones": total_anulaciones,
                "neta": utilidad_neta
            }
            return True, datos
            
        except Exception as e:
            return False, f"Error BD: Verifica que la columna de fecha se llame 'fecha' (Detalle: {e})"
        finally:
            conexion.close()
    
    @staticmethod
    def registrar_gasto(monto, descripcion, id_usuario):
        """Registra salidas de dinero (pagos, mantenimiento, etc.) forzando valores negativos."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            monto_negativo = -abs(monto) # Asegura que el valor sea matemáticamente negativo
            cursor.execute(
                "INSERT INTO Transaccion (id_usuario, tipo, monto, descripcion) VALUES (?, 'Gasto', ?, ?)",
                (id_usuario, monto_negativo, descripcion)
            )
            conexion.commit()
            return True, f"Gasto registrado exitosamente: ${abs(monto):,.2f}"
        except Exception as e:
            return False, f"Error al registrar el gasto: {e}"
        finally:
            conexion.close()

# ==========================================
# MÓDULO 9: CONFIGURACIÓN GENERAL
# ==========================================
class Configuracion:
    """Memoria de personalización del sistema (Logo y Nombre del gimnasio)."""
    
    @staticmethod
    def inicializar():
        """Crea la tabla de configuración (solo si no existe) para guardar el logo."""
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Configuracion (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                nombre_gym TEXT,
                ruta_logo TEXT
            )
        ''')
        # Inyecta los valores por defecto la primera vez que arranca el sistema
        cursor.execute("INSERT OR IGNORE INTO Configuracion (id, nombre_gym, ruta_logo) VALUES (1, 'Gym Pro', '')")
        conexion.commit()
        conexion.close()

    @staticmethod
    def cargar():
        """Devuelve el nombre y la imagen que el usuario haya guardado."""
        Configuracion.inicializar()
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre_gym, ruta_logo FROM Configuracion WHERE id = 1")
        resultado = cursor.fetchone()
        conexion.close()
        return resultado if resultado else ("Gym Pro", "")

    @staticmethod
    def guardar(nombre_gym, ruta_logo):
        """Sobrescribe la configuración anterior con los nuevos datos."""
        Configuracion.inicializar()
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE Configuracion SET nombre_gym = ?, ruta_logo = ? WHERE id = 1",
                (nombre_gym, ruta_logo)
            )
            conexion.commit()
            return True, "Configuración guardada permanentemente."
        except Exception as e:
            return False, f"Error al guardar en BD: {e}"
        finally:
            conexion.close()