import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
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
    
def guardar_turno_db(nombre,hora_inicio,hora_fin):
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
            (nombre, hora_inicio,hora_fin)
        )
        conn.commit()
        id_turno = cursor.lastrowid
        conn.close()
        return id_turno
    except mysql.connector.Error as err:
        messagebox.showerror("Error",f"No se pudo guardar el turno:\n{err}")
        return None
    
def guardar_turno_empleado_db(id_turno,id_empleado,fecha):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database = "kiosco"
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO turno_empleado (id_turno, id_empleado, dia) VALUES (%s, %s, %s)",
            (id_turno,id_empleado,fecha)
        )
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error",f"No se pudo asignar el turno al empleado: \n{err}")
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
            SELECT t.id_turno, t.nombre_turno, t.hora_inicio, t.hora_fin, e.nombre, te.dia
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

def editar_turno_db(id_turno, nombre, hora_inicio, hora_fin, id_empleado,dia_turno):
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


def cargar_turnos_por_dia(nombre_dia):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kiosco"
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT t.id_turno, t.nombre_turno, t.hora_inicio, t.hora_fin, e.nombre, te.dia
            FROM turno_empleado te
            JOIN turno t ON te.id_turno = t.id_turno
            JOIN empleado e ON te.id_empleado = e.id_empleado
            WHERE te.dia = %s
        """, (nombre_dia,))

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo cargar los turnos del día:\n{err}")
        return []

def hay_conflicto_turno(id_empleado, dia, hora_inicio, hora_fin, ignorar_id_turno=None):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kiosco"
        )
        cursor = conn.cursor()

        if ignorar_id_turno:
            cursor.execute("""
                SELECT t.hora_inicio, t.hora_fin
                FROM turno_empleado te
                JOIN turno t ON te.id_turno = t.id_turno
                WHERE te.id_empleado = %s AND te.dia = %s AND te.id_turno != %s
            """, (id_empleado, dia, ignorar_id_turno))
        else:
            cursor.execute("""
                SELECT t.hora_inicio, t.hora_fin
                FROM turno_empleado te
                JOIN turno t ON te.id_turno = t.id_turno
                WHERE te.id_empleado = %s AND te.dia = %s
            """, (id_empleado, dia))

        turnos = cursor.fetchall()
        conn.close()

        nueva_inicio = datetime.strptime(hora_inicio, "%H:%M:%S").time()
        nueva_fin = datetime.strptime(hora_fin, "%H:%M:%S").time()

        for inicio_raw, fin_raw in turnos:
            inicio = datetime.strptime(str(inicio_raw), "%H:%M:%S").time()
            fin = datetime.strptime(str(fin_raw), "%H:%M:%S").time()

            if nueva_inicio < fin and nueva_fin > inicio:
                return True

        return False

    except Exception as err:
        messagebox.showerror("Error de validación", f"No se pudo verificar conflictos:\n{err}")
        return True


turno_en_curso = None
inicio_turno = None

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

# 🖥️ Interfaz gráfica
class TurnoUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.configure(bg="#2c3e50",padx=20,pady=20)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        # 🔄 Cargar empleados desde la base
        empleados_raw = get_empleados_db()
        empleados_nombres = [nombre for _, _, nombre in empleados_raw]
        self.empleados_dict = {nombre: id_empleado for id_empleado, _, nombre in empleados_raw}


        style = ttk.Style()
        style.theme_use("clam")

        #----------Estilo para etiquetas y botones-------------
        style = ttk.Style()
        style.configure("Tlabel",background="red", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

        #--------Color de fondo de botones------------------
        style.map("TButton",
                  background=[("active", "#42ab49"), ("!disabled", "#89e186")],
                  foreground=[("!disabled", "white")])

        # Tipo de turno
        ttk.Label(self, text="Tipo de Turno",style="EtiquetaGrande.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.tipo_turno_combo = ttk.Combobox(self, values=["Mañana", "Tarde", "Noche"], state="readonly", width=27)
        self.tipo_turno_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.tipo_turno_combo.current(0)

        # Hora inicio
        ttk.Label(self, text="Hora Inicio",style="EtiquetaGrande.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.inicio_entry = ttk.Entry(self)
        self.inicio_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Hora fin
        ttk.Label(self, text="Hora Fin",style="EtiquetaGrande.TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.fin_entry = ttk.Entry(self)
        self.fin_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Empleado
        ttk.Label(self, text="Empleado",style="EtiquetaGrande.TLabel").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.empleado_combo = ttk.Combobox(self, values=empleados_nombres, state="readonly", width=27)
        self.empleado_combo.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        if empleados_nombres:
            self.empleado_combo.current(0)


        # Dia del turno
        ttk.Label(self,text="Dia",style="EtiquetaGrande.TLabel").grid(row=4,column=0, padx=10, pady=5, sticky="w")
        self.dia_combo = ttk.Combobox(self, values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"], state="readonly", width=27)
        self.dia_combo.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.dia_combo.current(0)

        # Filtro por dia
        ttk.Label(self,text="Filtrar por dia",style="EtiquetaGrande.TLabel").grid(row=10,column=0,padx=10,pady=5,sticky="w")
        self.filtro_dia_combo = ttk.Combobox(self, values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"], state="readonly", width=27)
        self.filtro_dia_combo.grid(row=10, column=1, padx=10, pady=5, sticky="w")
        self.filtro_dia_combo.bind("<<ComboboxSelected>>", self.filtrar_por_dia)




        # Botones de control de turno
        control_frame = tk.Frame(self,bg="#2c3e50")
        control_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)

        self.boton_comenzar = ttk.Button(control_frame,text="Comenzar Turno",style="BotonVerde.TButton",command=self.comenzar_turno)
        self.boton_comenzar.grid(row=0, column=0, padx=5, ipadx=5, ipady=3, sticky="ew")

        self.boton_cerrar = ttk.Button(control_frame,text="🔴 Cerrar Turno",style="BotonRojo.TButton",command=self.cerrar_turno)
        self.boton_cerrar.grid(row=0, column=1, padx=5, ipadx=5, ipady=3, sticky="ew")


        #-----------Estilo para las etiquetas-------------
        style.configure("EtiquetaGrande.TLabel",
                        background="#2c3e50",
                        foreground ="white",
                        font=("Segoe UI",12,"bold"))

        #------------Estilos para cada boton---------------
        style = ttk.Style()
        style.configure("BotonVerde.TButton",font=("Segoe UI", 8, "bold"), padding=6, background="#27ae60", foreground="white",relief="flat")
        style.configure("BotonAzul.TButton", font=("Segoe UI", 8, "bold"), padding=6, background="#2980b9", foreground="white",relief="flat")
        style.configure("BotonRojo.TButton", font=("Segoe UI", 8, "bold"), padding=6, background="#c0392b", foreground="white",relief="flat")

        #---------Efecto cuando se pase el mouse---------
        style.map("BotonVerde.TButton",
                  background=[("active", "#2ecc71")])
        
        style.map("BotonAzul.TButton",
                  background=[("active", "#3498db")])
        
        style.map("BotonRojo.TButton",
                  background=[("active", "#e74c3c")])
        
        #-------Contenedor para los 3 botones--------------
        boton_frame = tk.Frame(self,bg="#2c3e50")
        boton_frame.grid(row=5, column=0, columnspan=2, pady=(10, 10),sticky="ew")

        boton_frame.grid_columnconfigure(0, weight=1)
        boton_frame.grid_columnconfigure(1, weight=1)
        boton_frame.grid_columnconfigure(2, weight=1)


        # Crear turno
        self.boton_guardar = ttk.Button(boton_frame, text="Crear Turno",style="BotonVerde.TButton" ,command=self.crear_turno)
        self.boton_guardar.grid(row=0, column=0, padx=3, ipadx=5, ipady=3, sticky="ew")

        # Eliminar turno
        self.boton_eliminar = ttk.Button(boton_frame, text="🗑 Eliminar Turno",style="BotonRojo.TButton" ,command=self.eliminar_turno)
        self.boton_eliminar.grid(row=0, column=2, padx=3, ipadx=5, ipady=3, sticky="ew")

        # Editar turno
        self.boton_editar = ttk.Button(boton_frame, text="✏️ Editar Turno",style="BotonAzul.TButton" ,command=self.editar_turno)
        self.boton_editar.grid(row=0, column=1, padx=3, ipadx=5, ipady=3, sticky="ew")

        #--------Tabla estilizada y scrollbar-----------
        frame_tabla = tk.Frame(self,bg="#f5f6fa")
        frame_tabla.grid(row=7,column=0,columnspan=2,pady=10,sticky="nsew")

        # Tabla de turnos
        self.tree = ttk.Treeview(self, columns=("ID","Turno", "Inicio", "Fin", "Empleado","Dia"), show="headings", height=8)
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


        self.tree.heading("ID",text="ID")
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("Inicio", text="Hora Inicio")
        self.tree.heading("Fin", text="Hora Fin")
        self.tree.heading("Empleado", text="Empleado")
        self.tree.heading("Dia",text="Dia")

        self.tree.column("ID",width=50,stretch=False)
        self.tree.column("Turno", width=100)
        self.tree.column("Inicio", width=100)
        self.tree.column("Fin", width=100)
        self.tree.column("Empleado", width=150)
        self.tree.column("Dia",width=100)

        self.tree.bind("<<TreeviewSelect>>", self.cargar_turno_seleccionado)

        turnos_guardados = cargar_turnos_guardados()

        for id_turno,nombre,hora_inicio,hora_fin,empleado_nombre,dia in turnos_guardados:
            self.tree.insert("","end",values=(id_turno, nombre, hora_inicio, hora_fin, empleado_nombre,dia)) 

    def crear_turno(self):
        nombre = self.tipo_turno_combo.get()
        hora_inicio_raw = self.inicio_entry.get()
        hora_fin_raw = self.fin_entry.get()
        empleado_nombre = self.empleado_combo.get()
        id_empleado = self.empleados_dict.get(empleado_nombre)
        dia_turno = self.dia_combo.get()

        self.inicio_entry.delete(0, END)
        self.fin_entry.delete(0, END)

        if not hora_inicio_raw or not hora_fin_raw:
            messagebox.showerror("Error", "Debes ingresar la hora de inicio y la hora de fin del turno.")
            return

        
        hora_inicio = hora_inicio_raw + ":00"
        hora_fin = hora_fin_raw + ":00"

        #Validacion de que no se superpongan turnos
        if hay_conflicto_turno(id_empleado, dia_turno, hora_inicio, hora_fin):
            messagebox.showerror("Error", "No se puede agregar el turno: se superpone con otro turno ya existente.")
            return

        turno = Turno(None, nombre, hora_inicio, hora_fin)
        duracion = turno.duracion()

        id_turno = guardar_turno_db(nombre,hora_inicio,hora_fin)
        if id_turno:
            fecha_hoy = datetime.today().date()
            guardar_turno_empleado_db(id_turno,id_empleado,dia_turno)

            self.tree.insert("","end",values=(id_turno,nombre,hora_inicio,hora_fin,empleado_nombre,dia_turno))
        messagebox.showinfo("Turno creado", f"Turno '{nombre}' creado para {empleado_nombre} con duración de {duracion:.2f} horas.")

    def eliminar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccioná un turno en la tabla para eliminarlo.")
            return

        item = seleccion[0]
        valores = self.tree.item(item)["values"]
        id_turno = valores[0]

        eliminar_turno_db(id_turno)
        self.tree.delete(item)

        messagebox.showinfo("Turno eliminado", f"Turno '{valores[1]}' eliminado correctamente.")

    def cargar_turno_seleccionado(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = seleccion[0]
        valores = self.tree.item(item)["values"]

        self.tipo_turno_combo.set(valores[1])
        self.inicio_entry.delete(0, END)
        self.inicio_entry.insert(0, valores[2][:-3])
        self.fin_entry.delete(0, END)
        self.fin_entry.insert(0, valores[3][:-3])
        self.empleado_combo.set(valores[4])

    def editar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccioná un turno en la tabla para editarlo.")
            return

        item = seleccion[0]
        valores = self.tree.item(item)["values"]
        id_turno = valores[0]

        nombre = self.tipo_turno_combo.get()
        hora_inicio_raw = self.inicio_entry.get()
        hora_fin_raw = self.fin_entry.get()
        empleado = self.empleado_combo.get()
        id_empleado = self.empleados_dict.get(empleado)
        dia_turno = self.dia_combo.get()

        if not hora_inicio_raw or not hora_fin_raw:
            messagebox.showerror("Error", "Debes ingresar la hora de inicio y la hora de fin.")
            return

        hora_inicio = hora_inicio_raw + ":00"
        hora_fin = hora_fin_raw + ":00"
        
        #Validacion de conflicto ignorando el turno actual
        if hay_conflicto_turno(id_empleado, dia_turno, hora_inicio, hora_fin, ignorar_id_turno=id_turno):
            messagebox.showerror("Error", "No se puede editar el turno: se superpone con otro turno ya existente.")
            return
        editar_turno_db(id_turno, nombre, hora_inicio, hora_fin, id_empleado)
        self.tree.item(item,values=(id_turno, nombre, hora_inicio, hora_fin, empleado,dia_turno))

        messagebox.showinfo("Turno editado", f"Turno actualizado para {empleado}.")

    def filtrar_por_dia(self,event):
        dia_seleccionado = self.filtro_dia_combo.get()
        if not dia_seleccionado:
            return
        
        #Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        #Cargar turnos filtrados desde la db
        turnos_filtrados = cargar_turnos_por_dia(dia_seleccionado)

        for id_turno,nombre,hora_inicio,hora_fin,empleado_nombre,fecha in turnos_filtrados:
            self.tree.insert("", "end", values=(id_turno, nombre, hora_inicio, hora_fin, empleado_nombre, fecha))



    def comenzar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error","Selecciona un turno para comenzar")
            return
        
        item = seleccion[0]
        valores = self.tree.item(item)["values"]
        if len(valores) != 6:
            messagebox.showerror("Error",f"Turno incompleto:{valores}")
            return
        
        turno_id,nombre,hora_inicio,hora_fin,empleado,dia = valores
        turno = Turno(turno_id,nombre,hora_inicio,hora_fin)
        duracion = turno.duracion()

        #Guardar variables de turno activo
        global turno_en_curso,inicio_turno
        turno_en_curso = {
            "id":turno_id,
            "empleado":empleado,
            "inicio":datetime.now(),
            "duracion_estimada": duracion

        }
        inicio_turno = datetime.now()

        messagebox.showinfo("Turno inciciado",f"Turno '{nombre}' para {empleado} iniciado. \nDuracion estimada: {duracion:.2f} horas ")
        self.master.destroy() 
    def cerrar_turno(self):
        global turno_en_curso, inicio_turno

        if not turno_en_curso:
            messagebox.showerror("Error","No hay turno activo.")
            return

        inicio = turno_en_curso["inicio"]
        empleado = turno_en_curso["empleado"]
        fin = datetime.now()
        transcurrido = (fin - inicio).seconds / 3600

        messagebox.showinfo("Turno cerrado", f"Turno finalizado. \nTiempo trabajado: {transcurrido:.2f} horas.")
        self.master.destroy()

        turno_en_curso = None
        inicio_turno = None

# 🏁 Lanzar la app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Turnos")
    root.geometry("800x700")
    root.resizable(False,False)
    app = TurnoUI(master=root)
    app.mainloop()