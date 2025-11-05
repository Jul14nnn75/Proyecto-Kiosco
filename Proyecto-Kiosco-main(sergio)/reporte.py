import tkinter as tk
from tkinter import ttk, messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

class ReporteWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Configuración de la ventana
        self.title("📊 Enviar Reporte")
        self.geometry("500x400")
        self.configure(bg="#FFE5B4")
        self.resizable(False, False)
        
        # Centrar ventana
        self.transient(parent)
        self.grab_set()
        
        x = parent.winfo_x() + (parent.winfo_width() - 500) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 400) // 2
        self.geometry(f"+{x}+{y}")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self, bg="#FFE5B4", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        titulo_frame = tk.Frame(main_frame, bg="#FFE5B4")
        titulo_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(titulo_frame, text="📊 ENVIAR REPORTE", 
                font=("Segoe UI", 18, "bold"), 
                bg="#FFE5B4", fg="#2c3e50").pack()
        
        tk.Label(titulo_frame, text="Describa el problema o sugerencia", 
                font=("Segoe UI", 11), 
                bg="#FFE5B4", fg="#2c3e50").pack(pady=(5, 0))
        
        # Frame del formulario
        form_frame = tk.Frame(main_frame, bg="#FFFFFF", relief="flat", bd=1, padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)
        
        # Campo de email (opcional)
        tk.Label(form_frame, text="Su email (opcional):", 
                font=("Segoe UI", 10, "bold"), 
                bg="#FFFFFF", fg="#2c3e50").pack(anchor="w", pady=(0, 5))
        
        self.email_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=40)
        self.email_entry.pack(fill="x", pady=(0, 15), ipady=4)
        
        # Campo de reporte
        tk.Label(form_frame, text="Reporte:*", 
                font=("Segoe UI", 10, "bold"), 
                bg="#FFFFFF", fg="#2c3e50").pack(anchor="w", pady=(0, 5))
        
        self.reporte_text = tk.Text(form_frame, font=("Segoe UI", 11), 
                                   height=10, width=50, wrap="word")
        self.reporte_text.pack(fill="both", expand=True, pady=(0, 15))
        
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(self.reporte_text)
        scrollbar.pack(side="right", fill="y")
        self.reporte_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.reporte_text.yview)
        
        # Frame de botones
        btn_frame = tk.Frame(form_frame, bg="#FFFFFF")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        # Botón Enviar
        enviar_btn = tk.Button(btn_frame, text="📤 Enviar Reporte", 
                              command=self.enviar_reporte,
                              bg="#27ae60", fg="white", 
                              font=("Segoe UI", 11, "bold"),
                              relief="flat", padx=20, pady=10)
        enviar_btn.pack(side="right", padx=5)
        
        # Botón Cancelar
        cancelar_btn = tk.Button(btn_frame, text="❌ Cancelar", 
                                command=self.destroy,
                                bg="#e74c3c", fg="white", 
                                font=("Segoe UI", 11),
                                relief="flat", padx=20, pady=10)
        cancelar_btn.pack(side="right", padx=5)
        
        # Botón Limpiar
        limpiar_btn = tk.Button(btn_frame, text="Limpiar", 
                               command=self.limpiar_formulario,
                               bg="#95a5a6", fg="white", 
                               font=("Segoe UI", 11),
                               relief="flat", padx=15, pady=15)
        limpiar_btn.pack(side="left", padx=10)
        
        self.reporte_text.focus_set()
        self.bind('<Return>', lambda e: self.enviar_reporte())
        self.bind('<Escape>', lambda e: self.destroy())
    
    def limpiar_formulario(self):
        self.email_entry.delete(0, tk.END)
        self.reporte_text.delete(1.0, tk.END)
        self.reporte_text.focus_set()
    
    def enviar_reporte(self):
        """Envía el reporte por email REAL"""
        reporte = self.reporte_text.get(1.0, tk.END).strip()
        email_usuario = self.email_entry.get().strip()
        
        if not reporte:
            messagebox.showerror("Error", "Por favor, escriba su reporte antes de enviar.")
            self.reporte_text.focus_set()
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar envío", 
            "¿Está seguro de que desea enviar este reporte?"
        )
        
        if not confirmar:
            return
        
        try:
            # ✅ CONFIGURACIÓN REAL DEL EMAIL - MODIFICA ESTOS DATOS
            smtp_server = "smtp.gmail.com"  # Para Gmail
            smtp_port = 587
            email_from = "Software.Kiosco@gmail.com"  
            email_password = "feyu zacq rcsc jedy"  

            # Email de destino
            email_to = "thiagovillalba63@gmail.com"  
            
            # Crear mensaje
            mensaje = MIMEMultipart()
            mensaje['From'] = email_from
            mensaje['To'] = email_to
            mensaje['Subject'] = f"Reporte Sistema Kiosco - {self.obtener_fecha_hora()}"
            
            # Cuerpo del mensaje
            cuerpo = f"""
            NUEVO REPORTE DEL SISTEMA DE KIOSCO
            
            Fecha: {self.obtener_fecha_hora()}
            Email del usuario: {email_usuario if email_usuario else 'No proporcionado'}
            
            --- REPORTE ---
            {reporte}
            
            --- FIN DEL REPORTE ---
            
            Este es un mensaje automático del Sistema de Kiosco.
            """
            
            mensaje.attach(MIMEText(cuerpo, 'plain'))
            
            # ✅ ENVÍO REAL CON SMTP
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Seguridad
                server.login(email_from, email_password)
                server.send_message(mensaje)
            
            # Guardar copia local
            self.guardar_reporte_local(email_usuario, reporte)
            
            messagebox.showinfo(
                "✅ Reporte Enviado", 
                "Su reporte ha sido enviado CORRECTAMENTE al soporte técnico.\n"
                "Recibirá una respuesta pronto."
            )
            
            self.destroy()
            
        except Exception as e:
            error_msg = f"No se pudo enviar el reporte:\n{str(e)}"
            
            # Mensajes de error más específicos
            if "authentication" in str(e).lower():
                error_msg += "\n\n❌ Error de autenticación. Verifique email y contraseña."
            elif "connection" in str(e).lower():
                error_msg += "\n\n❌ Error de conexión. Verifique su internet."
            
            messagebox.showerror("Error de Envío", error_msg)
            
            # Guardar localmente como respaldo
            self.guardar_reporte_local(email_usuario, reporte)
            messagebox.showinfo(
                "Copia de Seguridad", 
                "El reporte se guardó localmente en data/reportes/"
            )
    
    def guardar_reporte_local(self, email, reporte):
        """Guarda el reporte localmente"""
        try:
            os.makedirs("data/reportes", exist_ok=True)
            
            archivo = f"data/reportes/reporte_{self.obtener_timestamp()}.txt"
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(f"Fecha: {self.obtener_fecha_hora()}\n")
                f.write(f"Email: {email if email else 'No proporcionado'}\n")
                f.write(f"Reporte:\n{reporte}\n")
                
        except Exception as e:
            print(f"Error guardando reporte local: {e}")
    
    def obtener_fecha_hora(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def obtener_timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")


# Función para abrir desde main_app.py
def abrir_reportes(parent):
    ventana_reportes = ReporteWindow(parent)
    return ventana_reportes


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = ReporteWindow(root)
    root.mainloop()