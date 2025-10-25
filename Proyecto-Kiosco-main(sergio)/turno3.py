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
            "INSERT INTO turno_empleado (id_turno, id_empleado, fecha) VALUES (%s, %s, %s)",
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

# 🖥️ Interfaz gráfica
class TurnoUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        # 🔄 Cargar empleados desde la base
        empleados_raw = get_empleados_db()
        empleados_nombres = [nombre for _, _, nombre in empleados_raw]
        self.empleados_dict = {nombre: id_empleado for id_empleado, _, nombre in empleados_raw}

        # Tipo de turno
        ttk.Label(self, text="Tipo de Turno").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.tipo_turno_combo = ttk.Combobox(self, values=["Mañana", "Tarde", "Noche"], state="readonly", width=27)
        self.tipo_turno_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.tipo_turno_combo.current(0)

        # Hora inicio
        ttk.Label(self, text="Hora Inicio").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.inicio_entry = ttk.Entry(self)
        self.inicio_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Hora fin
        ttk.Label(self, text="Hora Fin").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.fin_entry = ttk.Entry(self)
        self.fin_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Empleado
        ttk.Label(self, text="Empleado").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.empleado_combo = ttk.Combobox(self, values=empleados_nombres, state="readonly", width=27)
        self.empleado_combo.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        if empleados_nombres:
            self.empleado_combo.current(0)

        # Crear turno
        self.boton_guardar = ttk.Button(self, text="Crear Turno", command=self.crear_turno)
        self.boton_guardar.grid(row=4, column=0, columnspan=2, padx=10, pady=15, sticky="w")

        # Eliminar turno
        self.boton_eliminar = ttk.Button(self, text="Eliminar Turno", command=self.eliminar_turno)
        self.boton_eliminar.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        # Editar turno
        self.boton_editar = ttk.Button(self, text="Editar Turno", command=self.editar_turno)
        self.boton_editar.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Tabla de turnos
        self.tree = ttk.Treeview(self, columns=("ID","Turno", "Inicio", "Fin", "Empleado"), show="headings", height=8)
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.tree.heading("ID",text="ID")
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("Inicio", text="Hora Inicio")
        self.tree.heading("Fin", text="Hora Fin")
        self.tree.heading("Empleado", text="Empleado")

        self.tree.column("ID",width=0,stretch=False)
        self.tree.column("Turno", width=100)
        self.tree.column("Inicio", width=100)
        self.tree.column("Fin", width=100)
        self.tree.column("Empleado", width=150)

        self.tree.bind("<<TreeviewSelect>>", self.cargar_turno_seleccionado)

        turnos_guardados = cargar_turnos_guardados()

        for id_turno,nombre,hora_inicio,hora_fin,empleado_nombre in turnos_guardados:
            self.tree.insert("","end",values=(id_turno, nombre, hora_inicio, hora_fin, empleado_nombre)) 

    def crear_turno(self):
        nombre = self.tipo_turno_combo.get()
        hora_inicio_raw = self.inicio_entry.get()
        hora_fin_raw = self.fin_entry.get()
        empleado_nombre = self.empleado_combo.get()
        id_empleado = self.empleados_dict.get(empleado_nombre)

        self.inicio_entry.delete(0, END)
        self.fin_entry.delete(0, END)

        if not hora_inicio_raw or not hora_fin_raw:
            messagebox.showerror("Error", "Debes ingresar la hora de inicio y la hora de fin del turno.")
            return

        
        hora_inicio = hora_inicio_raw + ":00"
        hora_fin = hora_fin_raw + ":00"

        turno = Turno(None, nombre, hora_inicio, hora_fin)
        duracion = turno.duracion()

        id_turno = guardar_turno_db(nombre,hora_inicio,hora_fin)
        if id_turno:
            fecha_hoy = datetime.today().date()
            guardar_turno_empleado_db(id_turno,id_empleado,fecha_hoy)

            self.tree.insert("","end",values=(id_turno,nombre,hora_inicio,hora_fin,empleado_nombre))
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

        if not hora_inicio_raw or not hora_fin_raw:
            messagebox.showerror("Error", "Debes ingresar la hora de inicio y la hora de fin.")
            return

        hora_inicio = hora_inicio_raw + ":00"
        hora_fin = hora_fin_raw + ":00"

        editar_turno_db(id_turno, nombre, hora_inicio, hora_fin, id_empleado)
        self.tree.item(item,values=(id_turno, nombre, hora_inicio, hora_fin, empleado))

        messagebox.showinfo("Turno editado", f"Turno actualizado para {empleado}.")

# 🏁 Lanzar la app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Turnos")
    root.geometry("800x600")
    app = TurnoUI(master=root)
    app.mainloop()
