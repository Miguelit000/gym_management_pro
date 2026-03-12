from main import Usuario, inicializar_roles

print("--- Creando Usuario Administrador ---")

# 1. Por si acaso, nos aseguramos de que los roles existan
inicializar_roles()

# 2. Creamos a Miguel como Administrador (id_rol = 2)
# Puedes cambiar la clave a la que tú quieras, aquí usaré "admin123"
nuevo_admin = Usuario(id_rol=2, documento="12345678", nombre="Miguel Gomez", clave="admin123")

# 3. Lo registramos en la base de datos
nuevo_admin.registrar()