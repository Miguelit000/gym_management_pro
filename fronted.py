"""
=============================================================================
Gym Management Pro - Frontend (frontend.py)
Autor: Miguelit000
Descripción: Este archivo contiene toda la Interfaz Gráfica de Usuario (GUI)
construida con CustomTkinter. Maneja las ventanas, botones, tablas y la 
comunicación directa con la lógica de negocio en 'main.py'.
=============================================================================
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog 
from PIL import Image 
from main import Usuario

# ==========================================
# CONFIGURACIÓN DEL TEMA VISUAL
# ==========================================
ctk.set_appearance_mode("System")  # Adopta el modo oscuro o claro del sistema
ctk.set_default_color_theme("blue") # Tema de colores para los widgets

# =========================================================
# --- PANTALLA DE INICIO DE SESIÓN ---
# =========================================================
class VentanaLogin(ctk.CTk):
    """Ventana inicial del sistema. Controla el acceso mediante credenciales."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Gym Management Pro - Acceso")
        self.geometry("400x450")
        self.resizable(False, False) # Bloquea el cambio de tamaño de la ventana

        # Contenedor principal centrado
        self.frame = ctk.CTkFrame(master=self, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.label_titulo = ctk.CTkLabel(master=self.frame, text="Iniciar Sesión", font=("Roboto", 24, "bold"))
        self.label_titulo.place(x=50, y=45)

        # Campos de texto para credenciales
        self.entry_documento = ctk.CTkEntry(master=self.frame, width=220, placeholder_text="Documento")
        self.entry_documento.place(x=50, y=110)

        self.entry_clave = ctk.CTkEntry(master=self.frame, width=220, placeholder_text="Contraseña", show="*")
        self.entry_clave.place(x=50, y=165)

        self.btn_login = ctk.CTkButton(master=self.frame, width=220, text="Entrar", command=self.iniciar_sesion, corner_radius=6)
        self.btn_login.place(x=50, y=240)

    def iniciar_sesion(self):
        """Captura los datos, valida con la base de datos y abre el panel principal."""
        doc = self.entry_documento.get()
        pwd = self.entry_clave.get()

        usuario_valido = Usuario.autenticar(doc, pwd)

        if usuario_valido:
            self.destroy() # Cierra la ventana de login
            id_usuario, id_rol, nombre = usuario_valido
            # Abre el Dashboard pasándole los datos del usuario logueado
            dashboard = VentanaDashboard(id_usuario, id_rol, nombre)
            dashboard.mainloop()
        else:
            messagebox.showerror("Error de Acceso", "Documento o contraseña incorrectos.")
            
# =========================================================
# --- PANEL PRINCIPAL (DASHBOARD) ---
# =========================================================
class VentanaDashboard(ctk.CTk):
    """Ventana central de la aplicación. Contiene el menú lateral y el lienzo de trabajo."""
    
    def __init__(self, id_usuario, id_rol, nombre_usuario):
        super().__init__()
        
        # Guardamos la sesión actual para usarla en auditorías o permisos
        self.id_usuario = id_usuario
        self.id_rol = id_rol
        self.nombre_usuario = nombre_usuario

        self.title("Gym Management Pro - By Miguelit000")
        self.geometry("900x600")
        
        # Configuración de la cuadrícula: Columna 0 (Menú lateral), Columna 1 (Área principal)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- MENÚ LATERAL (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(11, weight=1) # Empuja el nombre de usuario hacia abajo

        # Cargamos el nombre y logo personalizado desde la base de datos
        from main import Configuracion
        nombre_guardado, ruta_logo_guardada = Configuracion.cargar()

        self.logo_img_label = ctk.CTkLabel(self.sidebar_frame, text="")
        self.logo_img_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text=nombre_guardado, font=("Roboto", 24, "bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(5, 20))

        # Intenta cargar la imagen si existe una ruta guardada
        if ruta_logo_guardada and ruta_logo_guardada != "":
            try:
                from PIL import Image
                imagen_pil = Image.open(ruta_logo_guardada)
                imagen_ctk = ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(100, 100))
                self.logo_img_label.configure(image=imagen_ctk)
            except Exception:
                pass # Si la imagen fue borrada del PC, ignora el error y no la muestra

        # --- BOTONES PÚBLICOS (Visibles para todos) ---
        self.btn_pos = ctk.CTkButton(self.sidebar_frame, text="Punto de Venta", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_pos)
        self.btn_pos.grid(row=2, column=0, padx=20, pady=10)

        self.btn_puerta = ctk.CTkButton(self.sidebar_frame, text="Control de Puerta", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_puerta)
        self.btn_puerta.grid(row=3, column=0, padx=20, pady=10)

        self.btn_clientes = ctk.CTkButton(self.sidebar_frame, text="Gestión de Clientes", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_clientes)
        self.btn_clientes.grid(row=4, column=0, padx=20, pady=10)

        self.btn_membresias = ctk.CTkButton(self.sidebar_frame, text="Vender Membresía", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_membresias)
        self.btn_membresias.grid(row=5, column=0, padx=20, pady=10)

        self.btn_inventario = ctk.CTkButton(self.sidebar_frame, text="Inventario", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_inventario)
        self.btn_inventario.grid(row=6, column=0, padx=20, pady=10)

        # --- BOTONES PRIVADOS (Solo Administradores - Rol 2) ---
        if self.id_rol == 2:
            self.btn_reportes = ctk.CTkButton(self.sidebar_frame, text="Reportes y Gastos", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_reportes)
            self.btn_reportes.grid(row=7, column=0, padx=20, pady=10)

            self.btn_usuarios = ctk.CTkButton(self.sidebar_frame, text="Gestión de Usuarios", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_usuarios)
            self.btn_usuarios.grid(row=8, column=0, padx=20, pady=10)

            self.btn_planes = ctk.CTkButton(self.sidebar_frame, text="Gestión de Planes", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_planes)
            self.btn_planes.grid(row=9, column=0, padx=20, pady=10)

            self.btn_config = ctk.CTkButton(self.sidebar_frame, text="Configuración", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_configuracion)
            self.btn_config.grid(row=10, column=0, padx=20, pady=10)

        # Etiqueta de sesión activa
        rol_texto = "Administrador" if self.id_rol == 2 else "Recepcionista"
        self.lbl_usuario = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.nombre_usuario}\n({rol_texto})")
        self.lbl_usuario.grid(row=11, column=0, padx=20, pady=20, sticky="s")

        # --- LIENZO PRINCIPAL ---
        # Aquí es donde se dibujarán todos los módulos dinámicamente
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Abre la vista de bienvenida por defecto
        self.mostrar_inicio()

    # =========================================================
    # --- FUNCIONES DE UTILIDAD ---
    # =========================================================
    def limpiar_main_frame(self):
        """Destruye todos los elementos visuales del área principal para dibujar una pantalla nueva."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        """Pantalla de bienvenida inicial al cargar el sistema."""
        self.limpiar_main_frame()
        lbl_bienvenida = ctk.CTkLabel(self.main_frame, text=f"¡Bienvenido, {self.nombre_usuario}!", font=("Roboto", 28, "bold"))
        lbl_bienvenida.pack(pady=(100, 20))
        lbl_instruccion = ctk.CTkLabel(self.main_frame, text="Selecciona un módulo en el menú lateral para comenzar.", font=("Roboto", 16))
        lbl_instruccion.pack()

    # =========================================================
    # --- MÓDULO: PUNTO DE VENTA (POS) ---
    # =========================================================
    def mostrar_pos(self):
        """Dibuja la interfaz del cajero y el catálogo interactivo de productos."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="🛒 Punto de Venta (POS)", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(20, 10))

        # Formulario de cobro
        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=10)

        self.entry_codigo = ctk.CTkEntry(frame_form, width=200, placeholder_text="Código del Producto")
        self.entry_codigo.grid(row=0, column=0, padx=10, pady=10)

        self.entry_cantidad = ctk.CTkEntry(frame_form, width=200, placeholder_text="Cantidad (Ej: 1)")
        self.entry_cantidad.grid(row=0, column=1, padx=10, pady=10)

        btn_vender = ctk.CTkButton(frame_form, text="💵 Procesar Venta", fg_color="green", hover_color="darkgreen", command=self.procesar_venta_gui)
        btn_vender.grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkLabel(self.main_frame, text="📦 Catálogo de Productos Disponibles", font=("Roboto", 16, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self.main_frame, text="*Haz un clic en un producto para pasarlo al cajero*", font=("Roboto", 12, "italic")).pack(pady=(0, 10))
        
        # Configuración de la Tabla (Treeview)
        from tkinter import ttk 
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=30)

        frame_tabla = ctk.CTkFrame(self.main_frame)
        frame_tabla.pack(pady=5, fill="both", expand=True, padx=40)

        columnas = ("codigo", "nombre", "precio", "stock")
        self.tabla_productos = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)
        
        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("nombre", text="Producto")
        self.tabla_productos.heading("precio", text="Precio de Venta")
        self.tabla_productos.heading("stock", text="Stock Disp.")

        self.tabla_productos.column("codigo", width=100, anchor="center")
        self.tabla_productos.column("nombre", width=300, anchor="w")
        self.tabla_productos.column("precio", width=120, anchor="center")
        self.tabla_productos.column("stock", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscroll=scrollbar.set)
        
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Evento: Clic para pasar datos al formulario
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto_tabla)
        
        self.cargar_tabla_pos()

    def cargar_tabla_pos(self):
        """Llena la tabla del catálogo interactivo consultando a la base de datos."""
        from main import Producto
        from tkinter import messagebox
        
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
            
        try:
            exito, productos = Producto.obtener_todos()
            if exito:
                if len(productos) == 0:
                    print("⚠️ Alerta: La base de datos dice que no hay ningún producto registrado.")
                for prod in productos:
                    self.tabla_productos.insert("", "end", values=(prod[0], prod[1], f"${prod[2]:,.2f}", prod[3]))
            else:
                messagebox.showerror("Error de Base de Datos", productos)
        except AttributeError:
            messagebox.showerror("Error Crítico", "Falta agregar la función 'obtener_todos()' en la clase Producto dentro de main.py")

    def seleccionar_producto_tabla(self, event):
        """Transfiere el código del producto clickeado en la tabla hacia el recuadro de venta."""
        seleccion = self.tabla_productos.selection()
        if seleccion:
            item = self.tabla_productos.item(seleccion[0])
            codigo_seleccionado = item['values'][0] 
            self.entry_codigo.delete(0, 'end')
            self.entry_codigo.insert(0, str(codigo_seleccionado))
            self.entry_cantidad.focus() # Mueve el cursor para escribir la cantidad automáticamente

    def procesar_venta_gui(self):
        """Ejecuta la venta descontando stock y sumando ingresos."""
        from main import Producto 
        from tkinter import messagebox
        codigo = self.entry_codigo.get()
        cantidad_str = self.entry_cantidad.get()

        if not codigo or not cantidad_str:
            messagebox.showwarning("Campos vacíos", "Ingresa el código y cantidad.")
            return

        try:
            cantidad = int(cantidad_str)
            exito, mensaje = Producto.vender(codigo, cantidad, self.id_usuario)
            
            if exito:
                messagebox.showinfo("Venta Procesada", mensaje)
                self.entry_codigo.delete(0, 'end')
                self.entry_cantidad.delete(0, 'end')
                self.cargar_tabla_pos() # Refresca el stock en la tabla en vivo
            else:
                messagebox.showwarning("Alerta", mensaje)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")

    # =========================================================
    # --- MÓDULO: CONFIGURACIÓN GENERAL ---
    # =========================================================
    def mostrar_configuracion(self):
        """Muestra el formulario para personalizar el nombre y logo del gimnasio."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="⚙️ Configuración del Gimnasio", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        self.entry_nombre_gym = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Nuevo nombre del gimnasio")
        self.entry_nombre_gym.pack(pady=15)

        btn_subir_logo = ctk.CTkButton(self.main_frame, text="🖼️ Subir Logo (PNG/JPG)", width=300, command=self.cargar_logo_temporal)
        btn_subir_logo.pack(pady=10)

        btn_guardar = ctk.CTkButton(self.main_frame, text="💾 Guardar Cambios", width=300, fg_color="green", hover_color="darkgreen", command=self.guardar_configuracion)
        btn_guardar.pack(pady=30)
        
        self.ruta_logo_temp = None

    def cargar_logo_temporal(self):
        """Abre el explorador de archivos para elegir una imagen."""
        ruta = filedialog.askopenfilename(title="Seleccionar Logo", filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            self.ruta_logo_temp = ruta
            messagebox.showinfo("Logo Seleccionado", "Imagen lista. Haz clic en 'Guardar Cambios' para aplicarla.")

    def guardar_configuracion(self):
        """Aplica los cambios en la UI y los guarda en la base de datos."""
        from main import Configuracion
        from PIL import Image
        
        nuevo_nombre = self.entry_nombre_gym.get()
        nombre_actual, logo_actual = Configuracion.cargar()
        nombre_final = nuevo_nombre if nuevo_nombre.strip() != "" else nombre_actual
        ruta_final = self.ruta_logo_temp if self.ruta_logo_temp else logo_actual
        
        # Aplica cambios en el menú visual
        self.logo_label.configure(text=nombre_final)
            
        if self.ruta_logo_temp:
            try:
                imagen_pil = Image.open(self.ruta_logo_temp)
                imagen_ctk = ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(100, 100))
                self.logo_img_label.configure(image=imagen_ctk)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen visualmente: {e}")
                return

        exito, mensaje = Configuracion.guardar(nombre_final, ruta_final)
        
        if exito:
            messagebox.showinfo("Éxito", "¡El sistema ha sido personalizado permanentemente!")
            self.entry_nombre_gym.delete(0, 'end')
            self.ruta_logo_temp = None 
        else:
            messagebox.showerror("Error al guardar", mensaje) 
        
    # =========================================================
    # --- MÓDULO: CONTROL DE PUERTA ---
    # =========================================================
    def mostrar_puerta(self):
        """Dibuja el semáforo para verificar el acceso de los clientes."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="🚪 Control de Acceso", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        self.entry_doc_puerta = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Escanea tarjeta o digita documento", font=("Roboto", 16))
        self.entry_doc_puerta.pack(pady=10)

        btn_verificar = ctk.CTkButton(self.main_frame, text="🔍 Verificar Acceso", width=300, command=self.verificar_acceso_gui)
        btn_verificar.pack(pady=10)

        # Semáforo visual
        self.frame_semaforo = ctk.CTkFrame(self.main_frame, width=450, height=150, corner_radius=15, fg_color="gray20")
        self.frame_semaforo.pack(pady=40)
        self.frame_semaforo.pack_propagate(False)
        self.lbl_mensaje_puerta = ctk.CTkLabel(self.frame_semaforo, text="Esperando lectura de tarjeta...", font=("Roboto", 18, "bold"), text_color="white", wraplength=400)
        self.lbl_mensaje_puerta.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def verificar_acceso_gui(self):
        """Evalúa los días de membresía y cambia el color del semáforo."""
        from main import Asistencia
        documento = self.entry_doc_puerta.get()
        
        if not documento:
            messagebox.showwarning("Campo vacío", "Por favor ingresa un documento.")
            return

        acceso_concedido, mensaje = Asistencia.registrar_entrada(documento)
        self.lbl_mensaje_puerta.configure(text=mensaje)

        if "Acceso Permitido" in mensaje:
            self.frame_semaforo.configure(fg_color="#228B22") # Verde
        elif "Acceso en gracia" in mensaje:
            self.frame_semaforo.configure(fg_color="#D4A017") # Naranja/Amarillo
            messagebox.showinfo("Aviso de Recepción", "Recuerda cobrarle a este cliente pronto.")
        else:
            self.frame_semaforo.configure(fg_color="#8B0000") # Rojo

        self.entry_doc_puerta.delete(0, 'end')
        
    # =========================================================
    # --- MÓDULO: REPORTES FINANCIEROS ---
    # =========================================================
    def mostrar_reportes(self):
        """Dibuja el cuadro de mandos con filtros históricos y tarjetas financieras."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="📊 Resumen Financiero", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(20, 10))

        # Filtro de meses
        frame_filtros = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_filtros.pack(pady=5)

        from datetime import datetime
        mes_actual = datetime.now().strftime('%Y-%m')

        ctk.CTkLabel(frame_filtros, text="📅 Período:").grid(row=0, column=0, padx=10)

        self.combo_periodo = ctk.CTkComboBox(frame_filtros, values=[mes_actual, "2026-02", "2026-01", "TODO"])
        self.combo_periodo.grid(row=0, column=1, padx=10)
        self.combo_periodo.set(mes_actual) 

        btn_filtrar = ctk.CTkButton(frame_filtros, text="🔍 Consultar", width=120, command=self.cargar_tarjetas_reporte)
        btn_filtrar.grid(row=0, column=2, padx=10)

        # Contenedor de las tarjetas (Se llenan dinámicamente)
        self.frame_cards = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_cards.pack(pady=10, fill="x", padx=40)
        self.frame_cards.grid_columnconfigure((0, 1), weight=1)

        # Formulario para registrar salidas de dinero
        frame_gasto = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_gasto.pack(pady=10, fill="x", padx=40)
        
        ctk.CTkLabel(frame_gasto, text="💸 Registrar Nuevo Gasto", font=("Roboto", 18, "bold")).pack(pady=5)
        self.gasto_desc = ctk.CTkEntry(frame_gasto, width=350, placeholder_text="Descripción (Ej: Pago de luz)")
        self.gasto_desc.pack(pady=5)
        self.gasto_monto = ctk.CTkEntry(frame_gasto, width=350, placeholder_text="Monto (Ej: 50000)")
        self.gasto_monto.pack(pady=5)
        
        btn_gasto = ctk.CTkButton(frame_gasto, text="Registrar Salida de Dinero", fg_color="#7a2424", hover_color="#5c1a1a", command=self.guardar_gasto_gui)
        btn_gasto.pack(pady=10)

        self.cargar_tarjetas_reporte()

    def cargar_tarjetas_reporte(self):
        """Pide los cálculos financieros a la base de datos y pinta los cuadros."""
        for widget in self.frame_cards.winfo_children():
            widget.destroy()

        from main import Dashboard
        periodo_seleccionado = self.combo_periodo.get()
        exito, datos = Dashboard.generar_reporte_financiero(periodo_seleccionado)

        if not exito:
            from tkinter import messagebox
            messagebox.showerror("Error", f"No se pudo cargar el reporte: {datos}")
            return

        # Tarjetas visuales
        card_ingresos = ctk.CTkFrame(self.frame_cards, corner_radius=10, fg_color="#1f532b")
        card_ingresos.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(card_ingresos, text="📈 Ingresos", font=("Roboto", 16), text_color="white").pack(pady=(15, 0))
        ctk.CTkLabel(card_ingresos, text=f"${datos['ingresos']:,.2f}", font=("Roboto", 24, "bold"), text_color="white").pack(pady=(5, 15))

        card_gastos = ctk.CTkFrame(self.frame_cards, corner_radius=10, fg_color="#7a2424")
        card_gastos.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(card_gastos, text="📉 Gastos", font=("Roboto", 16), text_color="white").pack(pady=(15, 0))
        ctk.CTkLabel(card_gastos, text=f"${datos['gastos']:,.2f}", font=("Roboto", 24, "bold"), text_color="white").pack(pady=(5, 15))

        card_anulaciones = ctk.CTkFrame(self.frame_cards, corner_radius=10, fg_color="#9c6614")
        card_anulaciones.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(card_anulaciones, text="⚠️ Anulaciones", font=("Roboto", 16), text_color="white").pack(pady=(15, 0))
        ctk.CTkLabel(card_anulaciones, text=f"${datos['anulaciones']:,.2f}", font=("Roboto", 24, "bold"), text_color="white").pack(pady=(5, 15))

        color_utilidad = "#1e3d59" if datos['neta'] >= 0 else "#7a2424"
        card_neta = ctk.CTkFrame(self.frame_cards, corner_radius=10, fg_color=color_utilidad)
        card_neta.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(card_neta, text="💰 UTILIDAD NETA", font=("Roboto", 18, "bold"), text_color="white").pack(pady=(15, 0))
        ctk.CTkLabel(card_neta, text=f"${datos['neta']:,.2f}", font=("Roboto", 28, "bold"), text_color="white").pack(pady=(5, 15))

    def guardar_gasto_gui(self):
        """Registra un egreso y recarga las gráficas."""
        from main import Dashboard
        from tkinter import messagebox
        desc = self.gasto_desc.get()
        monto_str = self.gasto_monto.get()

        if not desc or not monto_str:
            messagebox.showwarning("Atención", "Ingresa la descripción y el monto del gasto.")
            return

        try:
            monto = float(monto_str)
            exito, mensaje = Dashboard.registrar_gasto(monto, desc, self.id_usuario)
            
            if exito:
                messagebox.showinfo("Gasto Registrado", mensaje)
                self.gasto_desc.delete(0, 'end')
                self.gasto_monto.delete(0, 'end')
                self.cargar_tarjetas_reporte() 
            else:
                messagebox.showerror("Error", mensaje)
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
    
    # =========================================================
    # --- MÓDULO: GESTIÓN DE CLIENTES ---
    # =========================================================
    def mostrar_clientes(self):
        """Pantalla principal de creación y modificación de Clientes."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="👥 Gestión de Clientes", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(20, 10))

        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=10)

        self.entry_doc_cliente = ctk.CTkEntry(frame_form, width=200, placeholder_text="Documento (No editable al actualizar)")
        self.entry_doc_cliente.grid(row=0, column=0, padx=10, pady=10)

        self.entry_nom_cliente = ctk.CTkEntry(frame_form, width=200, placeholder_text="Nombre Completo")
        self.entry_nom_cliente.grid(row=0, column=1, padx=10, pady=10)

        self.entry_tel_cliente = ctk.CTkEntry(frame_form, width=200, placeholder_text="Teléfono Celular")
        self.entry_tel_cliente.grid(row=1, column=0, padx=10, pady=10)

        self.entry_email_cliente = ctk.CTkEntry(frame_form, width=200, placeholder_text="Correo Electrónico")
        self.entry_email_cliente.grid(row=1, column=1, padx=10, pady=10)

        frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="➕ Guardar Nuevo", fg_color="#28527a", width=120, command=self.registrar_cliente_gui).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="🔄 Actualizar", fg_color="#d4a373", text_color="black", hover_color="#faedcd", width=120, command=self.actualizar_cliente_gui).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="🗑️ Eliminar", fg_color="#7a2424", hover_color="#5c1a1a", width=120, command=self.eliminar_cliente_gui).grid(row=0, column=2, padx=5)
        ctk.CTkButton(frame_botones, text="🧹 Limpiar Campos", fg_color="gray", width=120, command=self.limpiar_form_cliente).grid(row=0, column=3, padx=5)

        # Configuración de la tabla de clientes
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=30)

        frame_tabla = ctk.CTkFrame(self.main_frame)
        frame_tabla.pack(pady=10, fill="both", expand=True, padx=40)

        columnas = ("doc", "nombre", "tel", "email")
        self.tabla_clientes = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)
        
        self.tabla_clientes.heading("doc", text="Documento")
        self.tabla_clientes.heading("nombre", text="Nombre")
        self.tabla_clientes.heading("tel", text="Teléfono")
        self.tabla_clientes.heading("email", text="Email")

        self.tabla_clientes.column("doc", width=120, anchor="center")
        self.tabla_clientes.column("nombre", width=250, anchor="w")
        self.tabla_clientes.column("tel", width=120, anchor="center")
        self.tabla_clientes.column("email", width=200, anchor="w")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_clientes.yview)
        self.tabla_clientes.configure(yscroll=scrollbar.set)
        
        self.tabla_clientes.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_clientes.bind("<<TreeviewSelect>>", self.seleccionar_cliente_tabla)
        self.cargar_tabla_clientes()

    def cargar_tabla_clientes(self):
        from main import Cliente
        for item in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(item)
            
        exito, clientes = Cliente.obtener_todos()
        if exito:
            for cli in clientes:
                self.tabla_clientes.insert("", "end", values=(cli[0], cli[1], cli[2], cli[3]))

    def seleccionar_cliente_tabla(self, event):
        seleccion = self.tabla_clientes.selection()
        if seleccion:
            item = self.tabla_clientes.item(seleccion[0])
            datos = item['values']
            
            self.entry_doc_cliente.configure(state="normal")
            self.limpiar_form_cliente(desbloquear=False)
            
            self.entry_doc_cliente.insert(0, str(datos[0]))
            self.entry_nom_cliente.insert(0, str(datos[1]))
            self.entry_tel_cliente.insert(0, str(datos[2]))
            self.entry_email_cliente.insert(0, str(datos[3]))
            
            self.entry_doc_cliente.configure(state="disabled")

    def limpiar_form_cliente(self, desbloquear=True):
        """Vacia las casillas. El parámetro desbloquear permite volver a escribir el documento."""
        if desbloquear:
            self.entry_doc_cliente.configure(state="normal")
        self.entry_doc_cliente.delete(0, 'end')
        self.entry_nom_cliente.delete(0, 'end')
        self.entry_tel_cliente.delete(0, 'end')
        self.entry_email_cliente.delete(0, 'end')

    def registrar_cliente_gui(self):
        from main import Cliente
        doc = self.entry_doc_cliente.get()
        nom = self.entry_nom_cliente.get()
        tel = self.entry_tel_cliente.get()
        email = self.entry_email_cliente.get()

        if not doc or not nom:
            messagebox.showwarning("Atención", "Mínimo se requiere Documento y Nombre.")
            return

        nuevo_cliente = Cliente(documento=doc, nombre=nom, telefono=tel, email=email)
        exito, mensaje = nuevo_cliente.registrar()

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_cliente()
            self.cargar_tabla_clientes()
        else:
            messagebox.showerror("Error", mensaje)

    def actualizar_cliente_gui(self):
        from main import Cliente
        doc = self.entry_doc_cliente.get()
        nom = self.entry_nom_cliente.get()
        tel = self.entry_tel_cliente.get()
        email = self.entry_email_cliente.get()

        if not doc:
            messagebox.showwarning("Atención", "Selecciona un cliente de la tabla primero.")
            return

        exito, mensaje = Cliente.actualizar(doc, nom, tel, email)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_cliente()
            self.cargar_tabla_clientes()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_cliente_gui(self):
        from main import Cliente
        doc = self.entry_doc_cliente.get()
        
        if not doc:
            messagebox.showwarning("Atención", "Selecciona un cliente de la tabla primero.")
            return
            
        respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Estás totalmente seguro de eliminar al cliente con documento {doc}?")
        if respuesta:
            exito, mensaje = Cliente.eliminar(doc)
            if exito:
                messagebox.showinfo("Eliminado", mensaje)
                self.limpiar_form_cliente()
                self.cargar_tabla_clientes()
            else:
                messagebox.showerror("Bloqueo", mensaje)
    
    # =========================================================
    # --- MÓDULO: GESTIÓN DE EQUIPO (USUARIOS) ---
    # =========================================================
    def mostrar_usuarios(self):
        """Pantalla exclusiva de administradores para manejar empleados."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="🛡️ Gestión del Equipo (Usuarios)", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(20, 10))

        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=10)

        self.entry_doc_user = ctk.CTkEntry(frame_form, width=250, placeholder_text="Documento (No editable al actualizar)")
        self.entry_doc_user.grid(row=0, column=0, padx=10, pady=10)

        self.entry_nom_user = ctk.CTkEntry(frame_form, width=250, placeholder_text="Nombre del Empleado")
        self.entry_nom_user.grid(row=0, column=1, padx=10, pady=10)

        self.combo_rol = ctk.CTkComboBox(frame_form, width=250, values=["Recepcionista", "Administrador"])
        self.combo_rol.grid(row=1, column=0, padx=10, pady=10)
        self.combo_rol.set("Recepcionista")

        self.entry_clave_user = ctk.CTkEntry(frame_form, width=250, placeholder_text="Contraseña (Déjala vacía si no cambias)", show="*")
        self.entry_clave_user.grid(row=1, column=1, padx=10, pady=10)

        frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="➕ Crear Cuenta", fg_color="#5a189a", width=120, command=self.registrar_usuario_gui).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="🔄 Actualizar", fg_color="#d4a373", text_color="black", hover_color="#faedcd", width=120, command=self.actualizar_usuario_gui).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="🗑️ Eliminar", fg_color="#7a2424", hover_color="#5c1a1a", width=120, command=self.eliminar_usuario_gui).grid(row=0, column=2, padx=5)
        ctk.CTkButton(frame_botones, text="🧹 Limpiar", fg_color="gray", width=120, command=self.limpiar_form_usuario).grid(row=0, column=3, padx=5)

        # Configuración de la tabla
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=30)

        frame_tabla = ctk.CTkFrame(self.main_frame)
        frame_tabla.pack(pady=10, fill="both", expand=True, padx=40)

        columnas = ("doc", "nombre", "rol")
        self.tabla_usuarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)
        
        self.tabla_usuarios.heading("doc", text="Documento")
        self.tabla_usuarios.heading("nombre", text="Nombre del Empleado")
        self.tabla_usuarios.heading("rol", text="Nivel de Acceso")

        self.tabla_usuarios.column("doc", width=150, anchor="center")
        self.tabla_usuarios.column("nombre", width=300, anchor="w")
        self.tabla_usuarios.column("rol", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscroll=scrollbar.set)
        
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.seleccionar_usuario_tabla)
        self.cargar_tabla_usuarios()

    def cargar_tabla_usuarios(self):
        from main import Usuario
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
            
        exito, usuarios = Usuario.obtener_todos()
        if exito:
            for usr in usuarios:
                self.tabla_usuarios.insert("", "end", values=(usr[0], usr[1], usr[2]))

    def seleccionar_usuario_tabla(self, event):
        seleccion = self.tabla_usuarios.selection()
        if seleccion:
            item = self.tabla_usuarios.item(seleccion[0])
            datos = item['values']
            
            self.entry_doc_user.configure(state="normal")
            self.limpiar_form_usuario(desbloquear=False)
            
            self.entry_doc_user.insert(0, str(datos[0]))
            self.entry_nom_user.insert(0, str(datos[1]))
            self.combo_rol.set(str(datos[2]))
            
            self.entry_doc_user.configure(state="disabled")

    def limpiar_form_usuario(self, desbloquear=True):
        if desbloquear:
            self.entry_doc_user.configure(state="normal")
        self.entry_doc_user.delete(0, 'end')
        self.entry_nom_user.delete(0, 'end')
        self.entry_clave_user.delete(0, 'end')
        self.combo_rol.set("Recepcionista")

    def registrar_usuario_gui(self):
        from main import Usuario
        doc = self.entry_doc_user.get()
        nom = self.entry_nom_user.get()
        rol_texto = self.combo_rol.get()
        clave = self.entry_clave_user.get()

        if not doc or not nom or not clave:
            messagebox.showwarning("Atención", "Todos los campos (incluida la contraseña) son obligatorios para crear.")
            return

        id_rol = 2 if rol_texto == "Administrador" else 3
        nuevo_user = Usuario(id_rol=id_rol, documento=doc, nombre=nom, clave=clave)
        exito, mensaje = nuevo_user.registrar()

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_usuario()
            self.cargar_tabla_usuarios()
        else:
            messagebox.showerror("Error", mensaje)

    def actualizar_usuario_gui(self):
        from main import Usuario
        doc = self.entry_doc_user.get()
        nom = self.entry_nom_user.get()
        rol_texto = self.combo_rol.get()
        clave = self.entry_clave_user.get() 

        if not doc:
            messagebox.showwarning("Atención", "Selecciona un usuario de la tabla.")
            return

        id_rol = 2 if rol_texto == "Administrador" else 3
        exito, mensaje = Usuario.actualizar(doc, nom, id_rol, clave)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_usuario()
            self.cargar_tabla_usuarios()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_usuario_gui(self):
        """Borra usuarios, exigiendo contraseña extra si es un Administrador."""
        from main import Usuario
        from tkinter import simpledialog 
        
        doc = self.entry_doc_user.get()
        nom = self.entry_nom_user.get()
        rol_texto = self.combo_rol.get()

        if not doc:
            messagebox.showwarning("Atención", "Selecciona un usuario de la tabla.")
            return

        # Blindaje de seguridad
        if rol_texto == "Administrador":
            clave_seguridad = simpledialog.askstring("Verificación Requerida", 
                                                     f"Para eliminar al administrador '{nom}', ingresa la contraseña de ESE administrador:", 
                                                     show='*')
            
            if not clave_seguridad: 
                return
                
            if not Usuario.autenticar(doc, clave_seguridad):
                messagebox.showerror("Acceso Denegado", "Contraseña incorrecta. Operación bloqueada.")
                return

        respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente la cuenta de {nom}?")
        if respuesta:
            exito, mensaje = Usuario.eliminar(doc)
            if exito:
                messagebox.showinfo("Eliminado", mensaje)
                self.limpiar_form_usuario()
                self.cargar_tabla_usuarios()
            else:
                messagebox.showerror("Bloqueo del Sistema", mensaje)
    
    # =========================================================
    # --- MÓDULO: ASIGNACIÓN DE MEMBRESÍAS ---
    # =========================================================
    def mostrar_membresias(self):
        """Pantalla para vincular un cliente a un plan contratado."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="🎟️ Gestión de Membresías", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(20, 10))

        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=10)

        self.entry_id_mem = ctk.CTkEntry(frame_form, width=80, placeholder_text="ID")
        self.entry_id_mem.grid(row=0, column=0, padx=5, pady=10)
        self.entry_id_mem.configure(state="disabled")

        self.entry_doc_membresia = ctk.CTkEntry(frame_form, width=220, placeholder_text="Documento del Cliente")
        self.entry_doc_membresia.grid(row=0, column=1, padx=10, pady=10)

        self.combo_plan = ctk.CTkComboBox(frame_form, width=250, values=[
            "Plan Mensual (30 días)", 
            "Plan Trimestral (90 días)", 
            "Plan Anual (365 días)"
        ])
        self.combo_plan.grid(row=0, column=2, padx=10, pady=10)
        self.combo_plan.set("Plan Mensual (30 días)")

        frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="⚡ Activar Nueva", fg_color="#228B22", hover_color="#006400", width=120, command=self.asignar_membresia_gui).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="🔄 Actualizar Plan", fg_color="#d4a373", text_color="black", hover_color="#faedcd", width=120, command=self.actualizar_membresia_gui).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="🗑️ Eliminar", fg_color="#7a2424", hover_color="#5c1a1a", width=120, command=self.eliminar_membresia_gui).grid(row=0, column=2, padx=5)
        ctk.CTkButton(frame_botones, text="🧹 Limpiar", fg_color="gray", width=120, command=self.limpiar_form_membresia).grid(row=0, column=3, padx=5)

        # Configuración de tabla
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=30)

        frame_tabla = ctk.CTkFrame(self.main_frame)
        frame_tabla.pack(pady=10, fill="both", expand=True, padx=40)

        columnas = ("id", "doc", "cliente", "plan", "vence")
        self.tabla_membresias = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)
        
        self.tabla_membresias.heading("id", text="ID Reg.")
        self.tabla_membresias.heading("doc", text="Doc. Cliente")
        self.tabla_membresias.heading("cliente", text="Nombre del Cliente")
        self.tabla_membresias.heading("plan", text="Plan Activo")
        self.tabla_membresias.heading("vence", text="Fecha Vencimiento")

        self.tabla_membresias.column("id", width=60, anchor="center")
        self.tabla_membresias.column("doc", width=120, anchor="center")
        self.tabla_membresias.column("cliente", width=250, anchor="w")
        self.tabla_membresias.column("plan", width=150, anchor="center")
        self.tabla_membresias.column("vence", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_membresias.yview)
        self.tabla_membresias.configure(yscroll=scrollbar.set)
        
        self.tabla_membresias.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_membresias.bind("<<TreeviewSelect>>", self.seleccionar_membresia_tabla)
        self.cargar_tabla_membresias()

    def cargar_tabla_membresias(self):
        from main import Membresia
        for item in self.tabla_membresias.get_children():
            self.tabla_membresias.delete(item)
            
        exito, membresias = Membresia.obtener_todas()
        if exito:
            for mem in membresias:
                self.tabla_membresias.insert("", "end", values=(mem[0], mem[1], mem[2], mem[3], mem[4]))

    def seleccionar_membresia_tabla(self, event):
        seleccion = self.tabla_membresias.selection()
        if seleccion:
            item = self.tabla_membresias.item(seleccion[0])
            datos = item['values']
            
            self.limpiar_form_membresia(desbloquear=True)
            
            self.entry_id_mem.insert(0, str(datos[0]))
            self.entry_doc_membresia.insert(0, str(datos[1]))
            if "Mensual" in str(datos[3]): self.combo_plan.set("Plan Mensual (30 días)")
            elif "Trimestral" in str(datos[3]): self.combo_plan.set("Plan Trimestral (90 días)")
            elif "Anual" in str(datos[3]): self.combo_plan.set("Plan Anual (365 días)")
            
            self.entry_id_mem.configure(state="disabled")
            self.entry_doc_membresia.configure(state="disabled")

    def limpiar_form_membresia(self, desbloquear=True):
        self.entry_id_mem.configure(state="normal")
        self.entry_doc_membresia.configure(state="normal")
        
        self.entry_id_mem.delete(0, 'end')
        self.entry_doc_membresia.delete(0, 'end')
        self.combo_plan.set("Plan Mensual (30 días)")
        
        if not desbloquear:
            self.entry_id_mem.configure(state="disabled")

    def asignar_membresia_gui(self):
        from main import Cliente, Membresia
        doc = self.entry_doc_membresia.get()
        plan_seleccionado = self.combo_plan.get()

        if not doc:
            messagebox.showwarning("Atención", "Ingresa el documento del cliente.")
            return

        cliente = Cliente.buscar_por_documento(doc)
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado. Regístralo en 'Gestión de Clientes'.")
            return

        id_cliente = cliente[0]
        dias, id_plan = (30, 1) if "Mensual" in plan_seleccionado else (90, 2) if "Trimestral" in plan_seleccionado else (365, 3)

        exito, mensaje = Membresia.crear_nueva(id_cliente, id_plan, dias)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_membresia()
            self.cargar_tabla_membresias()
        else:
            messagebox.showerror("Error", mensaje)

    def actualizar_membresia_gui(self):
        from main import Membresia
        id_mem = self.entry_id_mem.get()
        plan_seleccionado = self.combo_plan.get()

        if not id_mem:
            messagebox.showwarning("Atención", "Selecciona una membresía de la tabla para actualizarla.")
            return

        dias, id_plan = (30, 1) if "Mensual" in plan_seleccionado else (90, 2) if "Trimestral" in plan_seleccionado else (365, 3)

        exito, mensaje = Membresia.actualizar(id_mem, id_plan, dias)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_membresia()
            self.cargar_tabla_membresias()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_membresia_gui(self):
        from main import Membresia
        id_mem = self.entry_id_mem.get()
        doc = self.entry_doc_membresia.get()
        
        if not id_mem:
            messagebox.showwarning("Atención", "Selecciona una membresía de la tabla.")
            return

        respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar el registro de membresía del cliente {doc}?")
        if respuesta:
            exito, mensaje = Membresia.eliminar(id_mem)
            if exito:
                messagebox.showinfo("Eliminado", mensaje)
                self.limpiar_form_membresia()
                self.cargar_tabla_membresias()
            else:
                messagebox.showerror("Error", mensaje)
    
    # =========================================================
    # --- MÓDULO: GESTIÓN DE INVENTARIO ---
    # =========================================================
    def mostrar_inventario(self):
        """Pantalla de control para añadir artículos físicos al gimnasio."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="📦 Gestión de Inventario", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(20, 10))

        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=10)

        self.inv_codigo = ctk.CTkEntry(frame_form, width=200, placeholder_text="Código (No editable al actualizar)")
        self.inv_codigo.grid(row=0, column=0, padx=10, pady=10)
        
        self.inv_nombre = ctk.CTkEntry(frame_form, width=200, placeholder_text="Nombre del Producto")
        self.inv_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        self.inv_precio = ctk.CTkEntry(frame_form, width=200, placeholder_text="Precio de Venta ($)")
        self.inv_precio.grid(row=1, column=0, padx=10, pady=10)
        
        self.inv_stock = ctk.CTkEntry(frame_form, width=200, placeholder_text="Stock Disponible")
        self.inv_stock.grid(row=1, column=1, padx=10, pady=10)

        frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="➕ Crear Producto", fg_color="#28527a", width=120, command=self.registrar_producto_gui).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="🔄 Actualizar", fg_color="#d4a373", text_color="black", hover_color="#faedcd", width=120, command=self.actualizar_producto_gui).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="🗑️ Eliminar", fg_color="#7a2424", hover_color="#5c1a1a", width=120, command=self.eliminar_producto_gui).grid(row=0, column=2, padx=5)
        ctk.CTkButton(frame_botones, text="🧹 Limpiar", fg_color="gray", width=120, command=self.limpiar_form_inventario).grid(row=0, column=3, padx=5)

        # Configuración de tabla
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=30)

        frame_tabla = ctk.CTkFrame(self.main_frame)
        frame_tabla.pack(pady=10, fill="both", expand=True, padx=40)

        columnas = ("codigo", "nombre", "precio", "stock")
        self.tabla_inventario = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)
        
        self.tabla_inventario.heading("codigo", text="Código")
        self.tabla_inventario.heading("nombre", text="Producto")
        self.tabla_inventario.heading("precio", text="Precio de Venta")
        self.tabla_inventario.heading("stock", text="Stock Disponible")

        self.tabla_inventario.column("codigo", width=100, anchor="center")
        self.tabla_inventario.column("nombre", width=300, anchor="w")
        self.tabla_inventario.column("precio", width=120, anchor="center")
        self.tabla_inventario.column("stock", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_inventario.yview)
        self.tabla_inventario.configure(yscroll=scrollbar.set)
        
        self.tabla_inventario.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_inventario.bind("<<TreeviewSelect>>", self.seleccionar_producto_inv)
        self.cargar_tabla_inventario()

    def cargar_tabla_inventario(self):
        from main import Producto
        for item in self.tabla_inventario.get_children():
            self.tabla_inventario.delete(item)
            
        exito, productos = Producto.obtener_todos()
        if exito:
            for prod in productos:
                self.tabla_inventario.insert("", "end", values=(prod[0], prod[1], prod[2], prod[3]))

    def seleccionar_producto_inv(self, event):
        seleccion = self.tabla_inventario.selection()
        if seleccion:
            item = self.tabla_inventario.item(seleccion[0])
            datos = item['values']
            
            self.inv_codigo.configure(state="normal")
            self.limpiar_form_inventario(desbloquear=False)
            
            self.inv_codigo.insert(0, str(datos[0]))
            self.inv_nombre.insert(0, str(datos[1]))
            precio_limpio = str(datos[2]).replace("$", "").replace(",", "")
            self.inv_precio.insert(0, precio_limpio)
            self.inv_stock.insert(0, str(datos[3]))
            
            self.inv_codigo.configure(state="disabled")

    def limpiar_form_inventario(self, desbloquear=True):
        if desbloquear:
            self.inv_codigo.configure(state="normal")
        self.inv_codigo.delete(0, 'end')
        self.inv_nombre.delete(0, 'end')
        self.inv_precio.delete(0, 'end')
        self.inv_stock.delete(0, 'end')

    def registrar_producto_gui(self):
        from main import Producto
        cod = self.inv_codigo.get()
        nom = self.inv_nombre.get()
        pre_str = self.inv_precio.get()
        stk_str = self.inv_stock.get()

        if not cod or not nom or not pre_str or not stk_str:
            messagebox.showwarning("Atención", "Llena todos los campos para crear el producto.")
            return

        try:
            pre = float(pre_str)
            stk = int(stk_str)
            nuevo_prod = Producto(codigo=cod, nombre=nom, precio_venta=pre, stock=stk)
            exito, mensaje = nuevo_prod.registrar()
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_form_inventario()
                self.cargar_tabla_inventario()
            else:
                messagebox.showerror("Error", mensaje)
        except ValueError:
            messagebox.showerror("Error", "El precio y el stock deben ser valores numéricos.")

    def actualizar_producto_gui(self):
        from main import Producto
        cod = self.inv_codigo.get()
        nom = self.inv_nombre.get()
        pre_str = self.inv_precio.get()
        stk_str = self.inv_stock.get()

        if not cod:
            messagebox.showwarning("Atención", "Selecciona un producto de la tabla.")
            return

        try:
            pre = float(pre_str)
            stk = int(stk_str)
            exito, mensaje = Producto.actualizar(cod, nom, pre, stk)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_form_inventario()
                self.cargar_tabla_inventario()
            else:
                messagebox.showerror("Error", mensaje)
        except ValueError:
            messagebox.showerror("Error", "El precio y el stock deben ser valores numéricos.")

    def eliminar_producto_gui(self):
        from main import Producto
        cod = self.inv_codigo.get()
        
        if not cod:
            messagebox.showwarning("Atención", "Selecciona un producto de la tabla.")
            return

        respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente el producto {cod}?")
        if respuesta:
            exito, mensaje = Producto.eliminar(cod)
            if exito:
                messagebox.showinfo("Eliminado", mensaje)
                self.limpiar_form_inventario()
                self.cargar_tabla_inventario()
            else:
                messagebox.showerror("Error", mensaje)
            
    # =========================================================
    # --- MÓDULO: GESTIÓN DE PLANES ---
    # =========================================================
    def mostrar_planes(self):
        """Pantalla exclusiva de administradores para cambiar precios de membresías."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="📋 Configuración de Planes y Precios", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(20, 10))

        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=10)

        self.plan_id = ctk.CTkEntry(frame_form, width=80, placeholder_text="ID")
        self.plan_id.grid(row=0, column=0, padx=5, pady=10)
        self.plan_id.configure(state="disabled")

        self.plan_nombre = ctk.CTkEntry(frame_form, width=220, placeholder_text="Nombre (Ej: Plan Verano)")
        self.plan_nombre.grid(row=0, column=1, padx=10, pady=10)

        self.plan_dias = ctk.CTkEntry(frame_form, width=150, placeholder_text="Duración (Días)")
        self.plan_dias.grid(row=0, column=2, padx=10, pady=10)

        self.plan_precio = ctk.CTkEntry(frame_form, width=150, placeholder_text="Precio Total ($)")
        self.plan_precio.grid(row=0, column=3, padx=10, pady=10)

        frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="➕ Crear Plan", fg_color="#28527a", width=120, command=self.registrar_plan_gui).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="🔄 Actualizar Precio", fg_color="#d4a373", text_color="black", hover_color="#faedcd", width=150, command=self.actualizar_plan_gui).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="🗑️ Eliminar", fg_color="#7a2424", hover_color="#5c1a1a", width=120, command=self.eliminar_plan_gui).grid(row=0, column=2, padx=5)
        ctk.CTkButton(frame_botones, text="🧹 Limpiar", fg_color="gray", width=120, command=self.limpiar_form_plan).grid(row=0, column=3, padx=5)

        # Configuración de tabla
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=30)

        frame_tabla = ctk.CTkFrame(self.main_frame)
        frame_tabla.pack(pady=10, fill="both", expand=True, padx=40)

        columnas = ("id", "nombre", "dias", "precio")
        self.tabla_planes = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)
        
        self.tabla_planes.heading("id", text="ID")
        self.tabla_planes.heading("nombre", text="Nombre del Plan")
        self.tabla_planes.heading("dias", text="Días de Acceso")
        self.tabla_planes.heading("precio", text="Precio de Venta")

        self.tabla_planes.column("id", width=60, anchor="center")
        self.tabla_planes.column("nombre", width=300, anchor="w")
        self.tabla_planes.column("dias", width=150, anchor="center")
        self.tabla_planes.column("precio", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_planes.yview)
        self.tabla_planes.configure(yscroll=scrollbar.set)
        
        self.tabla_planes.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_planes.bind("<<TreeviewSelect>>", self.seleccionar_plan_tabla)
        self.cargar_tabla_planes()

    def cargar_tabla_planes(self):
        from main import Plan
        for item in self.tabla_planes.get_children():
            self.tabla_planes.delete(item)
            
        exito, planes = Plan.obtener_todos()
        if exito:
            for p in planes:
                self.tabla_planes.insert("", "end", values=(p[0], p[1], p[2], f"${p[3]:,.2f}"))

    def seleccionar_plan_tabla(self, event):
        seleccion = self.tabla_planes.selection()
        if seleccion:
            item = self.tabla_planes.item(seleccion[0])
            datos = item['values']
            
            self.limpiar_form_plan(desbloquear=True)
            
            self.plan_id.insert(0, str(datos[0]))
            self.plan_nombre.insert(0, str(datos[1]))
            self.plan_dias.insert(0, str(datos[2]))
            precio_limpio = str(datos[3]).replace("$", "").replace(",", "")
            self.plan_precio.insert(0, precio_limpio)
            
            self.plan_id.configure(state="disabled")

    def limpiar_form_plan(self, desbloquear=True):
        if desbloquear:
            self.plan_id.configure(state="normal")
        self.plan_id.delete(0, 'end')
        self.plan_nombre.delete(0, 'end')
        self.plan_dias.delete(0, 'end')
        self.plan_precio.delete(0, 'end')
        
        if not desbloquear:
            self.plan_id.configure(state="disabled")

    def registrar_plan_gui(self):
        from main import Plan
        from tkinter import messagebox
        nom = self.plan_nombre.get()
        dias_str = self.plan_dias.get()
        pre_str = self.plan_precio.get()

        if not nom or not dias_str or not pre_str:
            messagebox.showwarning("Atención", "Llena todos los campos para crear un plan.")
            return

        try:
            dias = int(dias_str)
            pre = float(pre_str)
            nuevo_plan = Plan(nombre=nom, dias_duracion=dias, precio_base=pre)
            exito, mensaje = nuevo_plan.registrar()
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_form_plan()
                self.cargar_tabla_planes()
            else:
                messagebox.showerror("Error", mensaje)
        except ValueError:
            messagebox.showerror("Error", "Días debe ser un número entero y Precio un número.")

    def actualizar_plan_gui(self):
        from main import Plan
        from tkinter import messagebox
        id_p = self.plan_id.get()
        nom = self.plan_nombre.get()
        dias_str = self.plan_dias.get()
        pre_str = self.plan_precio.get()

        if not id_p:
            messagebox.showwarning("Atención", "Selecciona un plan de la tabla.")
            return

        try:
            dias = int(dias_str)
            pre = float(pre_str)
            exito, mensaje = Plan.actualizar(id_p, nom, dias, pre)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_form_plan()
                self.cargar_tabla_planes()
            else:
                messagebox.showerror("Error", mensaje)
        except ValueError:
            messagebox.showerror("Error", "Días debe ser un número entero y Precio un número.")

    def eliminar_plan_gui(self):
        from main import Plan
        from tkinter import messagebox
        id_p = self.plan_id.get()
        nom = self.plan_nombre.get()
        
        if not id_p:
            messagebox.showwarning("Atención", "Selecciona un plan de la tabla.")
            return

        respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente el {nom}?")
        if respuesta:
            exito, mensaje = Plan.eliminar(id_p)
            if exito:
                messagebox.showinfo("Eliminado", mensaje)
                self.limpiar_form_plan()
                self.cargar_tabla_planes()
            else:
                messagebox.showerror("Error", mensaje)
            
# =========================================================
# --- EJECUCIÓN DEL PROGRAMA ---
# =========================================================
if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()