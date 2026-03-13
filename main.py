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
            return True, f"Éxito: Usuario '{self.nombre}' registrado correctamente."
            
        except sqlite3.IntegrityError:
            return False, f"Error: El documento '{self.documento}' ya está registrado."
            
        finally:
            conexion.close()
    @staticmethod
    def obtener_todos():
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            # Traemos el texto del rol en lugar del número para que la tabla se vea profesional
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
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            # Si el usuario escribió una clave nueva en la casilla, la encriptamos y la cambiamos
            if clave_nueva != "":
                import hashlib
                clave_hash = hashlib.sha256(clave_nueva.encode()).hexdigest()
                cursor.execute(
                    "UPDATE Usuario SET nombre = ?, id_rol = ?, clave_hash = ? WHERE documento = ?",
                    (nombre, id_rol, clave_hash, documento)
                )
            # Si dejó la casilla vacía, solo actualizamos el nombre y el rol (dejamos la clave intacta)
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
        import hashlib
        clave_hash = hashlib.sha256(clave.encode()).hexdigest()
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Traemos explícitamente el id_usuario, id_rol y nombre
        cursor.execute("SELECT id_usuario, id_rol, nombre FROM Usuario WHERE documento = ? AND clave_hash = ?", (documento, clave_hash))
        usuario = cursor.fetchone()
        conexion.close()
        
        return usuario # Devolverá (id_usuario, id_rol, nombre) o None

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
            return True, f"Cliente '{self.nombre}' registrado correctamente."
        except sqlite3.IntegrityError:
            return False, f"Error: El cliente con documento '{self.documento}' ya existe en el sistema."
        except Exception as e:
            return False, f"Error inesperado: {e}"
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
            # Intentamos borrar. Si tiene membresías compradas, SQLite lo impedirá por seguridad.
            cursor.execute("DELETE FROM Cliente WHERE documento = ?", (documento,))
            conexion.commit()
            return True, "Cliente eliminado del sistema."
        except sqlite3.IntegrityError:
            return False, "Bloqueo de Seguridad: No puedes eliminar a este cliente porque tiene un historial de membresías o asistencias guardado."
        except Exception as e:
            return False, f"Error al eliminar: {e}"
        finally:
            conexion.close()
        
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
            return True, f"Membresía registrada: Del {self.fecha_inicio} al {self.fecha_fin}."
        except Exception as e:
            return False, f"Error al registrar membresía: {e}"
        finally:
            conexion.close()
    
    @staticmethod
    def crear_nueva(id_cliente, id_plan, dias_duracion):
        fecha_inicio = date.today()
        # Calculamos la fecha de vencimiento sumando los días al día de hoy
        fecha_fin = fecha_inicio + timedelta(days=dias_duracion)
        
        nueva_membresia = Membresia(id_cliente, id_plan, fecha_inicio, fecha_fin)
        exito, mensaje = nueva_membresia.registrar()
        return exito, mensaje
    
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
    
    @staticmethod
    def obtener_todas():
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            # Unimos 3 tablas para traer el nombre del cliente y el nombre del plan
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
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            # Buscamos la fecha de inicio original para recalcular el nuevo vencimiento
            cursor.execute("SELECT fecha_inicio FROM Membresia WHERE id_membresia = ?", (id_membresia,))
            resultado = cursor.fetchone()
            if not resultado:
                return False, "Membresía no encontrada."
                
            fecha_inicio_str = resultado[0]
            from datetime import datetime, timedelta
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
            return True, f"Producto registrado: {self.nombre} (Stock inicial: {self.stock})"
        except sqlite3.IntegrityError:
            return False, f"Error: El código de producto '{self.codigo}' ya existe."
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
                return False, f"Producto con código '{codigo_producto}' no encontrado."
            
            id_prod, nombre, precio, stock_actual = producto
            
            if stock_actual < cantidad:
                return False, f"Alerta de Inventario: No hay suficiente stock de '{nombre}'. Disponible: {stock_actual}."
            
            total_venta = precio * cantidad
            nuevo_stock = stock_actual - cantidad
            
            cursor.execute("UPDATE Producto SET stock = ? WHERE id_producto = ?", (nuevo_stock, id_prod))
            
            descripcion_venta = f"Venta POS: {cantidad}x {nombre}"
            
            cursor.execute(
                "INSERT INTO Transaccion (id_usuario, tipo, monto, descripcion) VALUES (?, 'Ingreso', ?,?)",
                (id_usuario_vendedor, total_venta, descripcion_venta)
            )
            
            conexion.commit()
            return True, f"Venta exitosa: {cantidad}x {nombre}\nTotal: ${total_venta:,.2f}\n(Stock restante: {nuevo_stock})"
        
        except Exception as e:
            conexion.rollback()
            return False, f"Error crítico en la venta: {e}"
        finally:
            conexion.close()
            
    @staticmethod
    def agregar_stock(codigo_producto, cantidad_nueva):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT nombre, stock FROM Producto WHERE codigo = ?", (codigo_producto,))
            resultado = cursor.fetchone()
            
            if not resultado:
                return False, f"El producto con código '{codigo_producto}' no existe."
                
            nombre_prod, stock_actual = resultado
            nuevo_stock = stock_actual + cantidad_nueva
            
            cursor.execute("UPDATE Producto SET stock = ? WHERE codigo = ?", (nuevo_stock, codigo_producto))
            conexion.commit()
            
            return True, f"Stock actualizado.\nProducto: {nombre_prod}\nNuevo total en bodega: {nuevo_stock}"
            
        except Exception as e:
            return False, f"Error al actualizar inventario: {e}"
        finally:
            conexion.close()
            
    @staticmethod
    def obtener_todos():
        """Devuelve todos los productos registrados para llenar la tabla."""
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
                  
class Dashboard:
    @staticmethod
    def generar_reporte_financiero():
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        total_ingresos = 0.0
        total_gastos = 0.0
        total_anulaciones = 0.0
        utilidad_neta = 0.0
        
        try: 
            cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM Transaccion WHERE tipo = 'Ingreso'")
            fila_ingresos = cursor.fetchone()
            if fila_ingresos: total_ingresos = fila_ingresos[0]
            
            cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM Transaccion WHERE tipo = 'Gasto'")
            fila_gastos = cursor.fetchone()
            if fila_gastos: total_gastos = fila_gastos[0]
            
            cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM Transaccion WHERE tipo = 'Anulacion'")
            fila_anulaciones = cursor.fetchone()
            if fila_anulaciones: total_anulaciones = fila_anulaciones[0]
            
            utilidad_neta = total_ingresos + total_gastos + total_anulaciones
            
            # En lugar de imprimir, devolvemos un diccionario con los números limpios
            datos = {
                "ingresos": total_ingresos,
                "gastos": total_gastos,
                "anulaciones": total_anulaciones,
                "neta": utilidad_neta
            }
            return True, datos
            
        except Exception as e:
            return False, f"Error al generar el reporte: {e}"
            
        finally:
            conexion.close()
    
    @staticmethod
    def registrar_gasto(monto, descripcion, id_usuario):
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            # Guardamos el gasto como un valor negativo para que la suma del reporte cuadre perfecta
            monto_negativo = -abs(monto)
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