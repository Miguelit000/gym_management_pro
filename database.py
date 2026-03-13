"""
=============================================================================
Gym Management Pro - Estructura de Base de Datos (database.py)
Autor: Miguelit000
Descripción: Este script es el "Arquitecto" del sistema. Se ejecuta una sola 
vez al principio (o si se borra la base de datos) para construir todas las 
tablas y relaciones (Llaves Foráneas) necesarias en SQLite.
=============================================================================
"""

import sqlite3
import hashlib

def crear_base_datos():
    """Genera el archivo físico gym_pro.db y construye las 8 tablas fundamentales del sistema."""
    
    # Conecta o crea el archivo de la base de datos
    conexion = sqlite3.connect("gym_pro.db")
    cursor = conexion.cursor()
    
    # ---------------------------------------------------------
    # 1. TABLA: ROL (Niveles de acceso al sistema)
    # ---------------------------------------------------------
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Rol (
                id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
                )
            ''')
    
    # ---------------------------------------------------------
    # 2. TABLA: USUARIO (Empleados, Recepcionistas, Administradores)
    # ---------------------------------------------------------
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, 
                id_rol INTEGER,
                documento TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                clave_hash TEXT NOT NULL, -- La contraseña va encriptada por seguridad
                FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
                )
            ''')
    
    # ---------------------------------------------------------
    # 3. TABLA: CLIENTE (Personas inscritas en el gimnasio)
    # ---------------------------------------------------------
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                documento TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT
                )
            ''')
    
    # ---------------------------------------------------------
    # 4. TABLA: PLAN (Catálogo de membresías que se venden)
    # ---------------------------------------------------------
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Plan (
                id_plan INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dias_duracion INTEGER NOT NULL,
                precio_base REAL NOT NULL
                )
            ''')
    
    # ---------------------------------------------------------
    # 5. TABLA: MEMBRESÍA (El registro de qué plan compró un cliente y cuándo vence)
    # ---------------------------------------------------------
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Membresia (
                id_membresia INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER,
                id_plan INTEGER,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
                FOREIGN KEY (id_plan) REFERENCES Plan(id_plan)
                )
            ''')
    
    # ---------------------------------------------------------
    # 6. TABLA: TRANSACCIÓN (Libro de contabilidad: Ingresos, Gastos y Anulaciones)
    # ---------------------------------------------------------
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transaccion (
                id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER, -- Quién registró el movimiento en caja
                tipo TEXT NOT NULL, -- Puede ser: 'Ingreso', 'Gasto', 'Anulacion'
                monto REAL NOT NULL,
                descripcion TEXT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
                )
            ''')
    
    # ---------------------------------------------------------
    # 7. TABLA: AUDITORÍA (Historial de seguridad para rastrear fraudes o errores)
    # ---------------------------------------------------------
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Auditoria (
                id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                accion TEXT NOT NULL,
                tabla_afectada TEXT NOT NULL,
                registro_id INTEGER,
                valor_anterior TEXT,
                valor_nuevo TEXT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
                )
            ''')
    
    # ---------------------------------------------------------
    # 8. TABLA: PRODUCTO (Catálogo de artículos físicos para el Punto de Venta)
    # ---------------------------------------------------------
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Producto (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                precio_venta REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0
                )
            ''')
    
    # ---------------------------------------------------------
    # 9. Admin: Inyeccion de datos del usuario predeterminado
    # ---------------------------------------------------------
    # 1. insertar los roles (IGNORA si ya existen)
    roles_por_defecto = [("Socio",), ("Administrador",), ("Recepcionista",)]
    cursor.executemany("INSERT OR IGNORE INTO Rol (nombre) VALUES (?)", roles_por_defecto)
    
    #2. Insertar el administrador Maestro (Documento: 0, Clave: admin123)
    clave_maestra_encriptada = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute('''
            INSERT OR IGNORE INTO Usuario (id_rol, documento, nombre, clave_hash)
            VALUES (2, '0', 'Administrado Maestro', ?)
            ''', (clave_maestra_encriptada,))
    
    
    # Guarda los cambios y cierra el constructor
    conexion.commit()
    conexion.close()
    print("Base de datos 'gym_pro.db' verificada y estructurada con éxito")
    
# =========================================================
# --- PUNTO DE EJECUCIÓN ---
# Si corres este archivo directamente, construirá la base de datos
# =========================================================
if __name__ == "__main__":
    crear_base_datos()