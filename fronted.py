import customtkinter as ctk
from tkinter import messagebox, filedialog # Agregamos filedialog
from PIL import Image # Agregamos PIL para los logos
from main import Usuario

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

class VentanaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        
        self.title("Gym Management Pro - Acceso")
        self.geometry("400x450")
        self.resizable(False, False) 

        
        self.frame = ctk.CTkFrame(master=self, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        
        self.label_titulo = ctk.CTkLabel(master=self.frame, text="Iniciar Sesión", font=("Roboto", 24, "bold"))
        self.label_titulo.place(x=50, y=45)

        
        self.entry_documento = ctk.CTkEntry(master=self.frame, width=220, placeholder_text="Documento")
        self.entry_documento.place(x=50, y=110)

        self.entry_clave = ctk.CTkEntry(master=self.frame, width=220, placeholder_text="Contraseña", show="*")
        self.entry_clave.place(x=50, y=165)

        
        self.btn_login = ctk.CTkButton(master=self.frame, width=220, text="Entrar", command=self.iniciar_sesion, corner_radius=6)
        self.btn_login.place(x=50, y=240)

    def iniciar_sesion(self):
        doc = self.entry_documento.get()
        pwd = self.entry_clave.get()

        usuario_valido = Usuario.autenticar(doc, pwd)

        if usuario_valido:
            self.destroy() 
            
            nombre_usuario = usuario_valido[1]
            dashboard = VentanaDashboard(nombre_usuario)
            dashboard.mainloop()
        else:
            messagebox.showerror("Error de Acceso", "Documento o contraseña incorrectos.")
            
            
class VentanaDashboard(ctk.CTk):
    def __init__(self, nombre_usuario):
        super().__init__()

        self.title("Gym Management Pro - Panel Principal")
        self.geometry("900x600")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- MENÚ LATERAL (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1) # Empujamos el nombre de usuario más abajo

        self.logo_img_label = ctk.CTkLabel(self.sidebar_frame, text="")
        self.logo_img_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Gym Pro", font=("Roboto", 24, "bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(5, 20))

        # 1. Punto de Venta (Conectado a su pantalla)
        self.btn_pos = ctk.CTkButton(self.sidebar_frame, text="Punto de Venta", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_pos)
        self.btn_pos.grid(row=2, column=0, padx=20, pady=10)

        # 2. Control de Puerta (AQUÍ LE AGREGAMOS EL COMMAND)
        self.btn_puerta = ctk.CTkButton(self.sidebar_frame, text="Control de Puerta", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_puerta)
        self.btn_puerta.grid(row=3, column=0, padx=20, pady=10)

        # 3. Reportes Financieros (AQUÍ LE AGREGAMOS EL COMMAND)
        self.btn_reportes = ctk.CTkButton(self.sidebar_frame, text="Reportes Financieros", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_reportes)
        self.btn_reportes.grid(row=4, column=0, padx=20, pady=10)

        # 4. Gestión de Clientes (AQUÍ LE AGREGAMOS EL COMMAND)
        self.btn_clientes = ctk.CTkButton(self.sidebar_frame, text="Gestión de Clientes", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_clientes)
        self.btn_clientes.grid(row=5, column=0, padx=20, pady=10)

        # 5. Gestión de Usuarios (NUEVO)
        self.btn_usuarios = ctk.CTkButton(self.sidebar_frame, text="Gestión de Usuarios", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_usuarios)
        self.btn_usuarios.grid(row=6, column=0, padx=20, pady=10)
        
        # 6. Asignar Membresías (NUEVO)
        self.btn_membresias = ctk.CTkButton(self.sidebar_frame, text="Vender Membresía", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_membresias)
        self.btn_membresias.grid(row=7, column=0, padx=20, pady=10)

        # 7. Configuración (Asegúrate de cambiar su row a 8 para hacerle espacio)
        self.btn_config = ctk.CTkButton(self.sidebar_frame, text="Configuración", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.mostrar_configuracion)
        self.btn_config.grid(row=8, column=0, padx=20, pady=10)

        # Info del usuario conectado
        self.lbl_usuario = ctk.CTkLabel(self.sidebar_frame, text=f"👤 Usuario activo:\n{nombre_usuario}")
        self.lbl_usuario.grid(row=9, column=0, padx=20, pady=20, sticky="s")

        # --- ÁREA PRINCIPAL (MAIN CONTENT) ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.nombre_usuario = nombre_usuario
        self.mostrar_inicio()

    # (Mantén aquí tu función limpiar_main_frame, mostrar_inicio y las de configuración)

    # --- NUEVAS FUNCIONES PARA EL PUNTO DE VENTA ---
    def mostrar_pos(self):
        """Muestra la interfaz del cajero para vender productos."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="🛒 Punto de Venta (POS)", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        # Contenedor para alinear los inputs
        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=20)

        # Input de Código
        self.entry_codigo = ctk.CTkEntry(frame_form, width=200, placeholder_text="Código del Producto")
        self.entry_codigo.grid(row=0, column=0, padx=10, pady=10)

        # Input de Cantidad
        self.entry_cantidad = ctk.CTkEntry(frame_form, width=200, placeholder_text="Cantidad (Ej: 1)")
        self.entry_cantidad.grid(row=0, column=1, padx=10, pady=10)

        # Botón para procesar
        btn_vender = ctk.CTkButton(self.main_frame, text="💵 Procesar Venta", width=200, fg_color="green", hover_color="darkgreen", command=self.procesar_venta_gui)
        btn_vender.pack(pady=20)

    def procesar_venta_gui(self):
        """Lee los datos de la interfaz y los manda al backend."""
        from main import Producto # Importamos tu backend de productos
        
        codigo = self.entry_codigo.get()
        cantidad_str = self.entry_cantidad.get()

        if not codigo or not cantidad_str:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa el código y la cantidad.")
            return

        try:
            cantidad = int(cantidad_str)
            # Como aún no guardamos el ID exacto del usuario activo en el frontend, 
            # usaremos temporalmente el ID 1 (el administrador principal) para registrar la venta
            id_cajero_temporal = 1 
            
            # Llamamos a TU función del backend
            Producto.vender(codigo, cantidad, id_cajero_temporal)
            
            messagebox.showinfo("Proceso finalizado", "Venta procesada. Revisa la terminal para ver los detalles del recibo o posibles alertas de inventario.")
            
            # Limpiamos las casillas para la siguiente venta
            self.entry_codigo.delete(0, 'end')
            self.entry_cantidad.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")

    def limpiar_main_frame(self):
        """Borra todo lo que esté en el área principal para poner algo nuevo."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_main_frame()
        lbl_bienvenida = ctk.CTkLabel(self.main_frame, text=f"¡Bienvenido, {self.nombre_usuario}!", font=("Roboto", 28, "bold"))
        lbl_bienvenida.pack(pady=(100, 20))
        lbl_instruccion = ctk.CTkLabel(self.main_frame, text="Selecciona un módulo en el menú lateral para comenzar.", font=("Roboto", 16))
        lbl_instruccion.pack()

    def mostrar_configuracion(self):
        """Muestra el formulario para cambiar el nombre y el logo."""
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
        """Abre la ventana del PC para buscar una imagen."""
        ruta = filedialog.askopenfilename(title="Seleccionar Logo", filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            self.ruta_logo_temp = ruta
            messagebox.showinfo("Logo Seleccionado", "Imagen lista. Haz clic en 'Guardar Cambios' para aplicarla.")

    def guardar_configuracion(self):
        """Aplica los cambios al menú lateral."""
        nuevo_nombre = self.entry_nombre_gym.get()
        
        if nuevo_nombre.strip() != "":
            self.logo_label.configure(text=nuevo_nombre)
            
        if self.ruta_logo_temp:
            try:
                imagen_pil = Image.open(self.ruta_logo_temp)
                imagen_ctk = ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(100, 100))
                self.logo_img_label.configure(image=imagen_ctk)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
                
        messagebox.showinfo("Éxito", "¡El sistema ha sido personalizado!")
        self.entry_nombre_gym.delete(0, 'end') 
        
    def mostrar_pos(self):
        """Muestra la interfaz del cajero para vender productos."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="🛒 Punto de Venta (POS)", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        # Contenedor para alinear los inputs
        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=20)

        # Input de Código
        self.entry_codigo = ctk.CTkEntry(frame_form, width=200, placeholder_text="Código del Producto")
        self.entry_codigo.grid(row=0, column=0, padx=10, pady=10)

        # Input de Cantidad
        self.entry_cantidad = ctk.CTkEntry(frame_form, width=200, placeholder_text="Cantidad (Ej: 1)")
        self.entry_cantidad.grid(row=0, column=1, padx=10, pady=10)

        # Botón para procesar
        btn_vender = ctk.CTkButton(self.main_frame, text="💵 Procesar Venta", width=200, fg_color="green", hover_color="darkgreen", command=self.procesar_venta_gui)
        btn_vender.pack(pady=20)

    def procesar_venta_gui(self):
        from main import Producto 
        
        codigo = self.entry_codigo.get()
        cantidad_str = self.entry_cantidad.get()

        if not codigo or not cantidad_str:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa el código y la cantidad.")
            return

        try:
            cantidad = int(cantidad_str)
            id_cajero_temporal = 1 
            
            exito, mensaje = Producto.vender(codigo, cantidad, id_cajero_temporal)
            
            if exito:
                messagebox.showinfo("Venta Procesada", mensaje)
                self.entry_codigo.delete(0, 'end')
                self.entry_cantidad.delete(0, 'end')
            else:
                messagebox.showwarning("Alerta de Venta", mensaje)

        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            
    # --- NUEVAS FUNCIONES PARA EL CONTROL DE PUERTA ---
    def mostrar_puerta(self):
        """Muestra la interfaz del semáforo de acceso."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="🚪 Control de Acceso", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        # Input para simular el escáner de tarjeta o digitación manual
        self.entry_doc_puerta = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Escanea tarjeta o digita documento", font=("Roboto", 16))
        self.entry_doc_puerta.pack(pady=10)

        # Botón para verificar
        btn_verificar = ctk.CTkButton(self.main_frame, text="🔍 Verificar Acceso", width=300, command=self.verificar_acceso_gui)
        btn_verificar.pack(pady=10)

        # Semáforo Visual (Un recuadro que cambiará de color)
        self.frame_semaforo = ctk.CTkFrame(self.main_frame, width=450, height=150, corner_radius=15, fg_color="gray20")
        self.frame_semaforo.pack(pady=40)
        self.frame_semaforo.pack_propagate(False) # Evita que el recuadro se encoja al tamaño del texto

        # Texto dentro del semáforo
        self.lbl_mensaje_puerta = ctk.CTkLabel(self.frame_semaforo, text="Esperando lectura de tarjeta...", font=("Roboto", 18, "bold"), text_color="white", wraplength=400)
        self.lbl_mensaje_puerta.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def verificar_acceso_gui(self):
        """Conecta con el backend para validar la membresía y cambia los colores."""
        from main import Asistencia
        
        documento = self.entry_doc_puerta.get()
        
        if not documento:
            messagebox.showwarning("Campo vacío", "Por favor ingresa un documento.")
            return

        # Consultamos al backend que modificamos en el paso anterior
        acceso_concedido, mensaje = Asistencia.registrar_entrada(documento)

        # Actualizamos el texto del semáforo
        self.lbl_mensaje_puerta.configure(text=mensaje)

        # Lógica de colores (Semáforo)
        if "Acceso Permitido" in mensaje:
            self.frame_semaforo.configure(fg_color="#228B22") # Verde bosque
        elif "Acceso en gracia" in mensaje:
            self.frame_semaforo.configure(fg_color="#D4A017") # Amarillo/Dorado
            messagebox.showinfo("Aviso de Recepción", "Recuerda cobrarle a este cliente pronto.")
        else:
            self.frame_semaforo.configure(fg_color="#8B0000") # Rojo oscuro

        # Limpiamos el campo para el siguiente cliente
        self.entry_doc_puerta.delete(0, 'end')
        
    # --- NUEVAS FUNCIONES PARA LOS REPORTES ---
    def mostrar_reportes(self):
        """Consulta el backend y dibuja las tarjetas financieras."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="📊 Resumen Financiero", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        # Importamos el Dashboard de tu backend
        from main import Dashboard
        
        # Le pedimos los datos a la base de datos
        exito, datos = Dashboard.generar_reporte_financiero()

        if not exito:
            messagebox.showerror("Error", f"No se pudo cargar el reporte: {datos}")
            return

        # Contenedor (Cuadrícula) para organizar las 4 tarjetas
        frame_cards = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_cards.pack(pady=20, fill="x", padx=40)
        frame_cards.grid_columnconfigure((0, 1), weight=1)

        # 1. Tarjeta de Ingresos (Verde Oscuro)
        card_ingresos = ctk.CTkFrame(frame_cards, corner_radius=10, fg_color="#1f532b")
        card_ingresos.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(card_ingresos, text="📈 Total Ingresos", font=("Roboto", 16), text_color="white").pack(pady=(15, 0))
        ctk.CTkLabel(card_ingresos, text=f"${datos['ingresos']:,.2f}", font=("Roboto", 24, "bold"), text_color="white").pack(pady=(5, 15))

        # 2. Tarjeta de Gastos (Rojo Oscuro)
        card_gastos = ctk.CTkFrame(frame_cards, corner_radius=10, fg_color="#7a2424")
        card_gastos.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(card_gastos, text="📉 Total Gastos", font=("Roboto", 16), text_color="white").pack(pady=(15, 0))
        ctk.CTkLabel(card_gastos, text=f"${datos['gastos']:,.2f}", font=("Roboto", 24, "bold"), text_color="white").pack(pady=(5, 15))

        # 3. Tarjeta de Anulaciones (Naranja/Mostaza)
        card_anulaciones = ctk.CTkFrame(frame_cards, corner_radius=10, fg_color="#9c6614")
        card_anulaciones.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(card_anulaciones, text="⚠️ Total Anulaciones", font=("Roboto", 16), text_color="white").pack(pady=(15, 0))
        ctk.CTkLabel(card_anulaciones, text=f"${datos['anulaciones']:,.2f}", font=("Roboto", 24, "bold"), text_color="white").pack(pady=(5, 15))

        # 4. Tarjeta de Utilidad Neta (Azul Oscuro, o Rojo si hay pérdidas)
        color_utilidad = "#1e3d59" if datos['neta'] >= 0 else "#7a2424"
        card_neta = ctk.CTkFrame(frame_cards, corner_radius=10, fg_color=color_utilidad)
        card_neta.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(card_neta, text="💰 UTILIDAD NETA", font=("Roboto", 18, "bold"), text_color="white").pack(pady=(15, 0))
        ctk.CTkLabel(card_neta, text=f"${datos['neta']:,.2f}", font=("Roboto", 28, "bold"), text_color="white").pack(pady=(5, 15))
        
        # Botón para actualizar en tiempo real
        btn_refresh = ctk.CTkButton(self.main_frame, text="🔄 Actualizar Datos", command=self.mostrar_reportes)
        btn_refresh.pack(pady=30)
        
    def mostrar_clientes(self):
        """Muestra el formulario para inscribir nuevos miembros al gimnasio."""
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="👥 Registro de Nuevos Clientes", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        # Contenedor para el formulario (2 columnas x 2 filas)
        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=20)

        # Fila 1: Documento y Nombre
        self.entry_doc_cliente = ctk.CTkEntry(frame_form, width=250, placeholder_text="Documento de Identidad")
        self.entry_doc_cliente.grid(row=0, column=0, padx=10, pady=10)

        self.entry_nom_cliente = ctk.CTkEntry(frame_form, width=250, placeholder_text="Nombre Completo")
        self.entry_nom_cliente.grid(row=0, column=1, padx=10, pady=10)

        # Fila 2: Teléfono y Email
        self.entry_tel_cliente = ctk.CTkEntry(frame_form, width=250, placeholder_text="Teléfono Celular")
        self.entry_tel_cliente.grid(row=1, column=0, padx=10, pady=10)

        self.entry_email_cliente = ctk.CTkEntry(frame_form, width=250, placeholder_text="Correo Electrónico")
        self.entry_email_cliente.grid(row=1, column=1, padx=10, pady=10)

        # Botón para guardar
        btn_guardar_cliente = ctk.CTkButton(self.main_frame, text="💾 Inscribir Cliente", width=250, fg_color="#28527a", hover_color="#1a365d", command=self.registrar_cliente_gui)
        btn_guardar_cliente.pack(pady=30)

    def registrar_cliente_gui(self):
        """Captura los datos y los envía a la base de datos."""
        from main import Cliente
        
        doc = self.entry_doc_cliente.get()
        nom = self.entry_nom_cliente.get()
        tel = self.entry_tel_cliente.get()
        email = self.entry_email_cliente.get()

        # Validación básica para que no dejen campos en blanco
        if not doc or not nom or not tel or not email:
            messagebox.showwarning("Campos incompletos", "Por favor llena todos los datos del cliente para poder inscribirlo.")
            return

        # Instanciamos el cliente y llamamos al método modificado
        nuevo_cliente = Cliente(documento=doc, nombre=nom, telefono=tel, email=email)
        exito, mensaje = nuevo_cliente.registrar()

        if exito:
            messagebox.showinfo("Inscripción Exitosa", mensaje)
            # Limpiamos las casillas automáticamente
            self.entry_doc_cliente.delete(0, 'end')
            self.entry_nom_cliente.delete(0, 'end')
            self.entry_tel_cliente.delete(0, 'end')
            self.entry_email_cliente.delete(0, 'end')
        else:
            messagebox.showerror("Error en el Registro", mensaje)    
    
    # --- FUNCIONES PARA GESTIÓN DE USUARIOS ---
    def mostrar_usuarios(self):
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="🛡️ Creación de Usuarios", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=20)

        # Entradas de texto
        self.entry_doc_user = ctk.CTkEntry(frame_form, width=250, placeholder_text="Documento")
        self.entry_doc_user.grid(row=0, column=0, padx=10, pady=10)

        self.entry_nom_user = ctk.CTkEntry(frame_form, width=250, placeholder_text="Nombre del Empleado")
        self.entry_nom_user.grid(row=0, column=1, padx=10, pady=10)

        # Desplegable para el Rol
        self.combo_rol = ctk.CTkComboBox(frame_form, width=250, values=["Recepcionista", "Administrador"])
        self.combo_rol.grid(row=1, column=0, padx=10, pady=10)
        self.combo_rol.set("Recepcionista")

        self.entry_clave_user = ctk.CTkEntry(frame_form, width=250, placeholder_text="Contraseña", show="*")
        self.entry_clave_user.grid(row=1, column=1, padx=10, pady=10)

        # Botón
        btn_guardar_user = ctk.CTkButton(self.main_frame, text="Crear Cuenta", width=250, command=self.registrar_usuario_gui)
        btn_guardar_user.pack(pady=30)

    def registrar_usuario_gui(self):
        from main import Usuario
        
        doc = self.entry_doc_user.get()
        nom = self.entry_nom_user.get()
        rol_texto = self.combo_rol.get()
        clave = self.entry_clave_user.get()

        if not doc or not nom or not clave:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los datos.")
            return

        # ID 2 es Administrador, ID 3 es Recepcionista en tu DB
        id_rol = 2 if rol_texto == "Administrador" else 3

        nuevo_user = Usuario(id_rol=id_rol, documento=doc, nombre=nom, clave=clave)
        exito, mensaje = nuevo_user.registrar()

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.entry_doc_user.delete(0, 'end')
            self.entry_nom_user.delete(0, 'end')
            self.entry_clave_user.delete(0, 'end')
        else:
            messagebox.showerror("Error", mensaje)
            
    # --- FUNCIONES PARA VENDER MEMBRESÍAS ---
    def mostrar_membresias(self):
        self.limpiar_main_frame()
        
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="🎟️ Vender Membresía", font=("Roboto", 24, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        frame_form = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_form.pack(pady=20)

        # Entrada para el documento
        self.entry_doc_membresia = ctk.CTkEntry(frame_form, width=300, placeholder_text="Documento del Cliente")
        self.entry_doc_membresia.pack(pady=10)

        # Desplegable para elegir el plan
        self.combo_plan = ctk.CTkComboBox(frame_form, width=300, values=[
            "Plan Mensual (30 días)", 
            "Plan Trimestral (90 días)", 
            "Plan Anual (365 días)"
        ])
        self.combo_plan.pack(pady=10)
        self.combo_plan.set("Plan Mensual (30 días)")

        # Botón
        btn_activar = ctk.CTkButton(self.main_frame, text="⚡ Activar Plan", width=300, command=self.asignar_membresia_gui)
        btn_activar.pack(pady=30)

    def asignar_membresia_gui(self):
        from main import Cliente, Membresia
        
        doc = self.entry_doc_membresia.get()
        plan_seleccionado = self.combo_plan.get()

        if not doc:
            messagebox.showwarning("Atención", "Ingresa el documento del cliente.")
            return

        # 1. Buscamos al cliente en la base de datos
        cliente = Cliente.buscar_por_documento(doc)
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado. Regístralo primero en 'Gestión de Clientes'.")
            return

        id_cliente = cliente[0]

        # 2. Extraemos los días según el menú desplegable
        dias = 30
        id_plan = 1
        if "90" in plan_seleccionado:
            dias = 90
            id_plan = 2
        elif "365" in plan_seleccionado:
            dias = 365
            id_plan = 3

        # 3. Guardamos la membresía
        exito, mensaje = Membresia.crear_nueva(id_cliente, id_plan, dias)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.entry_doc_membresia.delete(0, 'end')
        else:
            messagebox.showerror("Error", mensaje)

if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()