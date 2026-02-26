import sqlite3

def crear_base_datos():
    
    conexion = sqlite3.connect("gym_pro.db")
    cursor = conexion.cursor()
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Rol (
                id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
                )
            ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, 
                id_rol INTEGER,
                documento TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                clave_hash TEXT NOT NULL,
                FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
                )
            ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                documento TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT
                )
            ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Plan (
                id_plan INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dias_duracion INTEGER NOT NULL,
                precio_base REAL NOT NULL
                )
            ''')
    
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
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transaccion (
                id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                tipo TEXT NOT NULL, -- 'Ingreso', 'Gasto', 'Anulacion'
                monto REAL NOT NULL,
                descripcion TEXT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
                )
            ''')
    
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
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Producto (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                precio_venta REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0
                )
            ''')
    
    conexion.commit()
    conexion.close()
    print("Base de datos 'gym_pro.db' creada con exito")
    
if __name__ == "__main__":
    crear_base_datos()
    