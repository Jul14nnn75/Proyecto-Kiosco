import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkinter import END

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

# Simulación temporal — luego se importa desde empleado.py
def get_empleados():
    return ["Ana", "Carlos", "Lucía", "Martín"]

class TurnoUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.turnos_creados = []  # Lista simulada de turnos
        self.crear_widgets()

    def crear_widgets(self):
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
        self.empleado_combo = ttk.Combobox(self, values=get_empleados(), state="readonly", width=27)
        self.empleado_combo.grid(row=3, column=1, padx=10, pady=5, sticky="w")
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
        self.tree = ttk.Treeview(self, columns=("Turno", "Inicio", "Fin", "Empleado"), show="headings", height=8)
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.tree.heading("Turno", text="Turno")
        self.tree.heading("Inicio", text="Hora Inicio")
        self.tree.heading("Fin", text="Hora Fin")
        self.tree.heading("Empleado", text="Empleado")

        self.tree.column("Turno", width=100)
        self.tree.column("Inicio", width=100)
        self.tree.column("Fin", width=100)
        self.tree.column("Empleado", width=150)

        # Activar carga automática al seleccionar
        self.tree.bind("<<TreeviewSelect>>", self.cargar_turno_seleccionado)

    def crear_turno(self):
        nombre = self.tipo_turno_combo.get()
        hora_inicio_raw = self.inicio_entry.get()
        hora_fin_raw = self.fin_entry.get()

        self.inicio_entry.delete(0, END)
        self.fin_entry.delete(0, END)

        if not hora_inicio_raw or not hora_fin_raw:
            messagebox.showerror("Error", "Debes ingresar la hora de inicio y la hora de fin del turno.")
            return

        empleado = self.empleado_combo.get()
        hora_inicio = hora_inicio_raw + ":00"
        hora_fin = hora_fin_raw + ":00"

        turno = Turno(None, nombre, hora_inicio, hora_fin)
        duracion = turno.duracion()

        # Guardar turno
        self.turnos_creados.append(nombre)

        # Mostrar en Treeview
        self.tree.insert("", "end", values=(nombre, hora_inicio, hora_fin, empleado))

        messagebox.showinfo("Turno creado", f"Turno '{nombre}' creado para {empleado} con duración de {duracion:.2f} horas.")

    def eliminar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccioná un turno en la tabla para eliminarlo.")
            return

        item = seleccion[0]
        valores = self.tree.item(item)["values"]
        nombre_turno = valores[0]

        if nombre_turno in self.turnos_creados:
            self.turnos_creados.remove(nombre_turno)

        self.tree.delete(item)

        messagebox.showinfo("Turno eliminado", f"Turno '{nombre_turno}' eliminado correctamente.")

    def cargar_turno_seleccionado(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = seleccion[0]
        valores = self.tree.item(item)["values"]

        self.tipo_turno_combo.set(valores[0])
        self.inicio_entry.delete(0, END)
        self.inicio_entry.insert(0, valores[1][:-3])  # Quita ":00"
        self.fin_entry.delete(0, END)
        self.fin_entry.insert(0, valores[2][:-3])
        self.empleado_combo.set(valores[3])

    def editar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccioná un turno en la tabla para editarlo.")
            return

        item = seleccion[0]
        nombre = self.tipo_turno_combo.get()
        hora_inicio_raw = self.inicio_entry.get()
        hora_fin_raw = self.fin_entry.get()
        empleado = self.empleado_combo.get()

        if not hora_inicio_raw or not hora_fin_raw:
            messagebox.showerror("Error", "Debes ingresar la hora de inicio y la hora de fin.")
            return

        hora_inicio = hora_inicio_raw + ":00"
        hora_fin = hora_fin_raw + ":00"

        self.tree.item(item, values=(nombre, hora_inicio, hora_fin, empleado))

        messagebox.showinfo("Turno editado", f"Turno actualizado para {empleado}.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Turnos")
    root.geometry("800x600")
    app = TurnoUI(master=root)
    app.mainloop()
