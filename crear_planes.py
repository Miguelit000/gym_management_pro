from main import Plan

print("--- 🚀 Creando Planes por Defecto en la Base de Datos ---")

# Creamos los 3 planes base (Puedes ajustar los precios como quieras)
plan1 = Plan(nombre="Plan Mensual", dias_duracion=30, precio_base=60000)
plan2 = Plan(nombre="Plan Trimestral", dias_duracion=90, precio_base=150000)
plan3 = Plan(nombre="Plan Anual", dias_duracion=365, precio_base=500000)

# Los guardamos en SQLite
plan1.registrar()
plan2.registrar()
plan3.registrar()

print("✅ ¡Planes creados con éxito!")