import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkinter import END
import mysql.connector

# 🔌 Conexión a la base de datos
def get_empleados_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="",  
            database="kiosco"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id_empleado, dni, nombre FROM empleado")
        empleados = cursor.fetchall()
        conn.close()
        return empleados
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
        return []
    
def guardar_turno_db(nombre, hora_inicio, hora_fin):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kiosco"
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO turno(nombre_turno, hora_inicio, hora_fin) VALUES (%s, %s, %s)",
            (nombre, hora_inicio, hora_fin)
        )
        conn.commit()
        id_turno = cursor.lastrowid
        conn.close()
        return id_turno
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo guardar el turno:\n{err}")
        return None
    
def guardar_turno_empleado_db(id_turno, id_empleado, fecha):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kiosco"
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO turno_empleado (id_turno, id_empleado, fecha) VALUES (%s, %s, %s)",
            (id_turno, id_empleado, fecha)
        )
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo asignar el turno al empleado: \n{err}")

def cargar_turnos_guardados():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kiosco"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id_turno, t.nombre_turno, t.hora_inicio, t.hora_fin, e.nombre
            FROM turno_empleado te
            JOIN turno t ON te.id_turno = t.id_turno
            JOIN empleado e ON te.id_empleado = e.id_empleado
        """)
        turnos = cursor.fetchall()
        conn.close()
        return turnos
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo cargar los turnos:\n{err}")
        return []
    
def eliminar_turno_db(id_turno):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kiosco"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM turno_empleado WHERE id_turno = %s", (id_turno,))
        cursor.execute("DELETE FROM turno WHERE id_turno = %s", (id_turno,))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo eliminar el turno:\n{err}")

def editar_turno_db(id_turno, nombre, hora_inicio, hora_fin, id_empleado):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kiosco"
        )
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE turno SET nombre_turno = %s, hora_inicio = %s, hora_fin = %s
            WHERE id_turno = %s
        """, (nombre, hora_inicio, hora_fin, id_turno))
        cursor.execute("""
            UPDATE turno_empleado SET id_empleado = %s
            WHERE id_turno = %s
        """, (id_empleado, id_turno))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo editar el turno:\n{err}")

# 🕒 Clase Turno
class Turno:
    def __init__(self, id_turno, nombre_turno, hora_inicio, hora_fin):
        self.id_turno = id_turno
        self.nombre_turno = nombre_turno
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def duracion(self):
        formato = "%H:%M:%S"
        inicio = datetime.strptime(str(self.hora_inicio), formato)
        fin = datetime.strptime(str(self.hora_fin), formato)
        return (fin - inicio).seconds / 3600

# 🖥️ Interfaz gráfica mejorada
class TurnoUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.tiempo_transcurrido = timedelta(0)
        self.cronometro_activo = False
        self.crear_widgets()
        self.actualizar_hora()

    def crear_widgets(self):
        # Configurar estilo minimalista
        self.configure(bg='#f8f9fa')
        style = ttk.Style()
        style.configure('TFrame', background='#f8f9fa')
        style.configure('TLabel', background='#f8f9fa', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('TCombobox', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))

        # Header con título y hora actual
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(header_frame, text="🕒 Gestión de Turnos", 
                 font=('Arial', 16, 'bold')).pack(side="left")
        
        self.hora_label = ttk.Label(header_frame, text="", 
                                   font=('Arial', 10), foreground='#666')
        self.hora_label.pack(side="right")

        # Frame principal con dos columnas
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Columna izquierda - Formulario
        form_frame = ttk.LabelFrame(main_frame, text="📋 Configurar Turno", padding=15)
        form_frame.pack(side="left", fill="y", padx=(0, 15))

        # Tipo de turno
        ttk.Label(form_frame, text="Tipo de Turno").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.tipo_turno_combo = ttk.Combobox(form_frame, values=["Mañana", "Tarde", "Noche"], 
                                           state="readonly", width=20)
        self.tipo_turno_combo.grid(row=0, column=1, padx=5, pady=8)
        self.tipo_turno_combo.current(0)

        # Hora inicio
        ttk.Label(form_frame, text="Hora Inicio").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.inicio_entry = ttk.Entry(form_frame, width=22)
        self.inicio_entry.grid(row=1, column=1, padx=5, pady=8)
        self.inicio_entry.insert(0, datetime.now().strftime("%H:%M"))

        # Hora fin
        ttk.Label(form_frame, text="Hora Fin").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.fin_entry = ttk.Entry(form_frame, width=22)
        self.fin_entry.grid(row=2, column=1, padx=5, pady=8)
        self.fin_entry.insert(0, "18:00")

        # Empleado
        ttk.Label(form_frame, text="Empleado").grid(row=3, column=0, padx=5, pady=8, sticky="w")
        
        # Cargar empleados desde la base
        empleados_raw = get_empleados_db()
        empleados_nombres = [nombre for _, _, nombre in empleados_raw]
        self.empleados_dict = {nombre: id_empleado for id_empleado, _, nombre in empleados_raw}
        
        self.empleado_combo = ttk.Combobox(form_frame, values=empleados_nombres, 
                                         state="readonly", width=20)
        self.empleado_combo.grid(row=3, column=1, padx=5, pady=8)
        if empleados_nombres:
            self.empleado_combo.current(0)

        # Botones de acciones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        self.boton_crear = ttk.Button(btn_frame, text="➕ Crear Turno", 
                                    command=self.crear_turno, width=15)
        self.boton_crear.pack(side="left", padx=5)

        self.boton_editar = ttk.Button(btn_frame, text="✏️ Editar Turno", 
                                     command=self.editar_turno, width=15)
        self.boton_editar.pack(side="left", padx=5)

        self.boton_eliminar = ttk.Button(btn_frame, text="🗑️ Eliminar Turno", 
                                       command=self.eliminar_turno, width=15)
        self.boton_eliminar.pack(side="left", padx=5)

        # Columna derecha - Cronómetro y lista
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        # Cronómetro
        crono_frame = ttk.LabelFrame(right_frame, text="⏱️ Cronómetro de Turno", padding=15)
        crono_frame.pack(fill="x", pady=(0, 15))

        self.crono_label = ttk.Label(crono_frame, text="00:00:00", 
                                   font=('Arial', 24, 'bold'), foreground='#2c3e50')
        self.crono_label.pack(pady=10)

        crono_btn_frame = ttk.Frame(crono_frame)
        crono_btn_frame.pack(pady=10)

        self.boton_iniciar = ttk.Button(crono_btn_frame, text="▶️ Iniciar Turno", 
                                      command=self.iniciar_cronometro, width=15)
        self.boton_iniciar.pack(side="left", padx=5)

        self.boton_pausar = ttk.Button(crono_btn_frame, text="⏸️ Pausar", 
                                     command=self.pausar_cronometro, width=12, state="disabled")
        self.boton_pausar.pack(side="left", padx=5)

        self.boton_cerrar = ttk.Button(crono_btn_frame, text="⏹️ Cerrar Turno", 
                                     command=self.cerrar_turno, width=15, state="disabled")
        self.boton_cerrar.pack(side="left", padx=5)

        # Tabla de turnos
        table_frame = ttk.LabelFrame(right_frame, text="📊 Turnos Registrados", padding=10)
        table_frame.pack(fill="both", expand=True)

        # Crear Treeview con scrollbar
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Turno", "Inicio", "Fin", "Empleado"), 
                               show="headings", height=12)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("Inicio", text="Hora Inicio")
        self.tree.heading("Fin", text="Hora Fin")
        self.tree.heading("Empleado", text="Empleado")

        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("Turno", width=100)
        self.tree.column("Inicio", width=100)
        self.tree.column("Fin", width=100)
        self.tree.column("Empleado", width=150)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.cargar_turno_seleccionado)

        # Cargar turnos existentes
        self.cargar_turnos()

    def actualizar_hora(self):
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.hora_label.config(text=f"🕐 {ahora}")
        self.after(1000, self.actualizar_hora)

    def cargar_turnos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar turnos de la base de datos
        turnos_guardados = cargar_turnos_guardados()
        for id_turno, nombre, hora_inicio, hora_fin, empleado_nombre in turnos_guardados:
            self.tree.insert("", "end", values=(id_turno, nombre, hora_inicio, hora_fin, empleado_nombre))

    def iniciar_cronometro(self):
        if not self.cronometro_activo:
            self.cronometro_activo = True
            self.boton_iniciar.config(state="disabled")
            self.boton_pausar.config(state="normal")
            self.boton_cerrar.config(state="normal")
            self.inicio_cronometro = datetime.now()
            self.actualizar_cronometro()

    def pausar_cronometro(self):
        self.cronometro_activo = False
        self.boton_iniciar.config(state="normal")
        self.boton_pausar.config(state="disabled")

    def cerrar_turno(self):
        self.cronometro_activo = False
        self.tiempo_transcurrido = timedelta(0)
        self.crono_label.config(text="00:00:00")
        self.boton_iniciar.config(state="normal")
        self.boton_pausar.config(state="disabled")
        self.boton_cerrar.config(state="disabled")
        messagebox.showinfo("Turno Cerrado", "El turno ha sido cerrado correctamente.")

    def actualizar_cronometro(self):
        if self.cronometro_activo:
            self.tiempo_transcurrido = datetime.now() - self.inicio_cronometro
            horas = int(self.tiempo_transcurrido.total_seconds() // 3600)
            minutos = int((self.tiempo_transcurrido.total_seconds() % 3600) // 60)
            segundos = int(self.tiempo_transcurrido.total_seconds() % 60)
            
            tiempo_str = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            self.crono_label.config(text=tiempo_str)
            self.after(1000, self.actualizar_cronometro)

    def crear_turno(self):
        nombre = self.tipo_turno_combo.get()
        hora_inicio_raw = self.inicio_entry.get()
        hora_fin_raw = self.fin_entry.get()
        empleado_nombre = self.empleado_combo.get()
        id_empleado = self.empleados_dict.get(empleado_nombre)

        if not all([hora_inicio_raw, hora_fin_raw, empleado_nombre]):
            messagebox.showerror("Error", "Complete todos los campos requeridos.")
            return

        # Validar formato de hora
        try:
            datetime.strptime(hora_inicio_raw, "%H:%M")
            datetime.strptime(hora_fin_raw, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM")
            return

        hora_inicio = hora_inicio_raw + ":00"
        hora_fin = hora_fin_raw + ":00"

        turno = Turno(None, nombre, hora_inicio, hora_fin)
        duracion = turno.duracion()

        id_turno = guardar_turno_db(nombre, hora_inicio, hora_fin)
        if id_turno:
            fecha_hoy = datetime.today().date()
            guardar_turno_empleado_db(id_turno, id_empleado, fecha_hoy)
            
            # Actualizar tabla
            self.cargar_turnos()
            
            # Limpiar campos
            self.inicio_entry.delete(0, END)
            self.fin_entry.delete(0, END)
            self.inicio_entry.insert(0, datetime.now().strftime("%H:%M"))
            self.fin_entry.insert(0, "18:00")
            
            messagebox.showinfo("Turno Creado", 
                              f"✅ Turno '{nombre}' creado para {empleado_nombre}\n"
                              f"⏰ Duración: {duracion:.2f} horas")

    def eliminar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un turno de la tabla para eliminarlo.")
            return

        item = seleccion[0]
        valores = self.tree.item(item)["values"]
        id_turno = valores[0]

        confirmar = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de eliminar el turno '{valores[1]}'?")
        if confirmar:
            eliminar_turno_db(id_turno)
            self.tree.delete(item)
            messagebox.showinfo("Turno Eliminado", f"Turno '{valores[1]}' eliminado correctamente.")

    def cargar_turno_seleccionado(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = seleccion[0]
        valores = self.tree.item(item)["values"]

        self.tipo_turno_combo.set(valores[1])
        self.inicio_entry.delete(0, END)
        self.inicio_entry.insert(0, valores[2][:-3])  # Remover segundos
        self.fin_entry.delete(0, END)
        self.fin_entry.insert(0, valores[3][:-3])    # Remover segundos
        self.empleado_combo.set(valores[4])

    def editar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un turno de la tabla para editarlo.")
            return

        item = seleccion[0]
        valores = self.tree.item(item)["values"]
        id_turno = valores[0]

        nombre = self.tipo_turno_combo.get()
        hora_inicio_raw = self.inicio_entry.get()
        hora_fin_raw = self.fin_entry.get()
        empleado = self.empleado_combo.get()
        id_empleado = self.empleados_dict.get(empleado)

        if not all([hora_inicio_raw, hora_fin_raw, empleado]):
            messagebox.showerror("Error", "Complete todos los campos requeridos.")
            return

        # Validar formato de hora
        try:
            datetime.strptime(hora_inicio_raw, "%H:%M")
            datetime.strptime(hora_fin_raw, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM")
            return

        hora_inicio = hora_inicio_raw + ":00"
        hora_fin = hora_fin_raw + ":00"

        editar_turno_db(id_turno, nombre, hora_inicio, hora_fin, id_empleado)
        
        # Actualizar tabla
        self.cargar_turnos()
        
        messagebox.showinfo("Turno Editado", f"✅ Turno actualizado para {empleado}")

# 🏁 Lanzar la app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Turnos - Sistema Kiosco")
    root.geometry("1000x700")
    root.configure(bg='#f8f9fa')
    
    # Centrar ventana
    root.eval('tk::PlaceWindow . center')
    
    app = TurnoUI(master=root)
    app.mainloop()