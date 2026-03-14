# 🏋️‍♂️ Gym Management Pro

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-darkblue)
![Status](https://img.shields.io/badge/Estado-Completado-success)

**Gym Management Pro** es un sistema integral de escritorio (ERP/POS) diseñado para administrar gimnasios y centros deportivos. Permite gestionar clientes, vender membresías, controlar el acceso a las instalaciones, llevar el inventario de productos y generar reportes financieros en tiempo real.

Desarrollado con una arquitectura limpia en Python, utilizando **CustomTkinter** para una interfaz moderna y **SQLite** como motor de base de datos embebido.

---

## ✨ Características Principales

* 🔐 **Seguridad y Roles:** Autenticación de usuarios con contraseñas encriptadas (SHA-256). Accesos restringidos según el rol (Administrador vs. Recepcionista).
* 👥 **Gestión de Clientes y Planes (CRUD):** Registro de clientes y configuración dinámica de planes (mensualidades, trimestres, anualidades) con precios ajustables.
* 🎟️ **Control de Membresías:** Asignación de planes a clientes con cálculo automático de fechas de vencimiento.
* 🚪 **Control de Puerta (Semaforización):** Módulo de acceso que verifica el estado de la membresía en tiempo real. Incluye alertas de "Días de gracia" y denegación de acceso para planes vencidos.
* 🛒 **Punto de Venta (POS) e Inventario:** Catálogo interactivo para vender productos físicos (agua, suplementos, etc.). Descuenta el stock automáticamente y suma el dinero a la caja.
* 📊 **Reportes Financieros:** Dashboard dinámico que calcula Ingresos, Gastos, Anulaciones y Utilidad Neta, con filtros por historial mensual.
* ⚙️ **Personalización:** Permite cambiar el nombre del gimnasio y subir un logotipo permanente desde la interfaz gráfica.
* 🚀 **Auto-Despliegue:** El sistema construye su propia base de datos estructural e inyecta un Administrador Maestro automáticamente al ejecutarse por primera vez.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Base de Datos:** SQLite3 (Nativa)
* **Interfaz Gráfica:** CustomTkinter (UI Moderna y Responsiva)
* **Procesamiento de Imágenes:** Pillow (PIL)
* **Seguridad:** Hashlib (SHA-256)

---

## 📥 Instalación y Ejecución Local

Sigue estos pasos para clonar y ejecutar el proyecto en tu máquina local:



### 1. Clonar el repositorio
```bash
git clone [https://github.com/Miguelit000/gym_management_pro.git](https://github.com/Miguelit000/gym_management_pro.git)
cd gym_management_pro 

### 2. Crear un Entorno Virtual (Recomendado)
```bash
#En Windows
python -m venv env
env/Scripts\activate
#En Linux/Mac
python3 -m venv env
source env/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install customtkinter pillow
```

### 4. Ejecutar la Aplicacion

El sistema creara automaticamente el archivo gym_pro.db en el primer arranque.
```bash
python fronted.py
```

## 🔑 Credenciales de Acceso por Defecto
Al ejecutar el proyecto por primera vez, el sistema genera un superusuario para que puedas ingresar al panel de administración:

Documento: 0

Contraseña: admin123

(Se recomienda cambiar la contraseña o crear un nuevo administrador una vez dentro del sistema).

## 📸 Capturas de Pantalla

> (imagenes/1.png)
> (imagenes/2.png)
> (imagenes/3.png)
> (imagenes/4.png)
> (imagenes/5.png)
> (imagenes/6.png)
> (imagenes/7.png)
> (imagenes/8.png)
> (imagenes/9.png)


## 👨‍💻 Autor
Miguelit000

Proyecto desarrollado como demostración de habilidades en lógica de programación, bases de datos relacionales y diseño de interfaces GUI con Python.