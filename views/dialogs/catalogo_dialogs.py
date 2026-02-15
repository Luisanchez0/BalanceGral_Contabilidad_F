"""
views/dialogs/catalogo_dialogs.py
Diálogos para gestión del catálogo
"""

import tkinter as tk
from tkinter import ttk, messagebox
from utils.helpers import CATEGORIAS_COMBO, formatear_moneda


class DialogoCatalogo(tk.Toplevel):
    """Diálogo para ver el catálogo"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.title("Catálogo de Cuentas")
        self.geometry("800x600")
        self.transient(parent)
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        tk.Label(self, text="CATÁLOGO DE CUENTAS", font=('Arial', 16, 'bold')).pack(pady=10)
        
        catalogo = self.controller.obtener_catalogo_completo()
        
        for categoria, nombre in [('ACTIVO_CIRCULANTE', 'ACTIVO CIRCULANTE'),
                                   ('ACTIVO_NO_CIRCULANTE', 'ACTIVO NO CIRCULANTE'),
                                   ('PASIVO_LARGO_PLAZO', 'PASIVO LARGO PLAZO'),
                                   ('PASIVO_CORTO_PLAZO', 'PASIVO CORTO PLAZO'),
                                   ('CAPITAL', 'CAPITAL')]:
            frame = tk.Frame(self, relief=tk.GROOVE, bd=2)
            frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(frame, text=nombre, font=('Arial', 11, 'bold'), bg='#BBDEFB').pack(fill=tk.X)
            
            for cuenta, valor in catalogo[categoria].items():
                fila = tk.Frame(frame)
                fila.pack(fill=tk.X, padx=5)
                tk.Label(fila, text=cuenta, anchor='w').pack(side=tk.LEFT, fill=tk.X, expand=True)
                tk.Label(fila, text=formatear_moneda(valor), anchor='e').pack(side=tk.RIGHT)


class DialogoEditarCatalogo(tk.Toplevel):
    """Diálogo para editar el catálogo"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.cambios_realizados = False
        self.entries = {}
        
        self.title("Editar Catálogo")
        self.geometry("700x600")
        self.transient(parent)
        self.grab_set()
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        tk.Label(self, text="Editar Catálogo", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Crear campos editables
        catalogo = self.controller.obtener_catalogo_completo()
        
        for categoria, nombre in [('ACTIVO_CIRCULANTE', 'ACTIVO CIRCULANTE'),
                                   ('ACTIVO_NO_CIRCULANTE', 'ACTIVO NO CIRCULANTE')]:
            frame = tk.Frame(self)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(frame, text=nombre, font=('Arial', 11, 'bold'), bg='#BBDEFB').pack(fill=tk.X)
            
            for cuenta, valor in catalogo[categoria].items():
                fila = tk.Frame(frame)
                fila.pack(fill=tk.X)
                tk.Label(fila, text=cuenta, width=30, anchor='w').pack(side=tk.LEFT)
                
                var = tk.StringVar(value=f"{valor:.2f}")
                tk.Entry(fila, textvariable=var, width=15, justify='right').pack(side=tk.LEFT)
                self.entries[(categoria, cuenta)] = var
        
        tk.Button(self, text="💾 Guardar", command=self._guardar, bg='#4CAF50', fg='white',
                 font=('Arial', 10, 'bold'), padx=20, pady=8).pack(pady=20)
    
    def _guardar(self):
        try:
            for (categoria, cuenta), var in self.entries.items():
                valor = float(var.get())
                self.controller.modificar_cuenta(categoria, cuenta, valor)
            
            self.cambios_realizados = True
            messagebox.showinfo("Éxito", "Catálogo actualizado")
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos")


class DialogoAgregarCuenta(tk.Toplevel):
    """Diálogo para agregar cuenta"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.cuenta_agregada = False
        
        self.title("Agregar Cuenta")
        self.geometry("400x300")
        self.transient(parent)
        self.grab_set()
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        tk.Label(self, text="Agregar Nueva Cuenta", font=('Arial', 14, 'bold')).pack(pady=20)
        
        tk.Label(self, text="Categoría:", font=('Arial', 11)).pack(pady=5)
        self.categoria_var = tk.StringVar()
        combo = ttk.Combobox(self, textvariable=self.categoria_var,
                            values=list(CATEGORIAS_COMBO.values()),
                            state='readonly', width=30)
        combo.pack(pady=5)
        combo.set('Activo Circulante')
        
        tk.Label(self, text="Nombre:", font=('Arial', 11)).pack(pady=5)
        self.nombre_var = tk.StringVar()
        tk.Entry(self, textvariable=self.nombre_var, width=35).pack(pady=5)
        
        tk.Label(self, text="Valor inicial:", font=('Arial', 11)).pack(pady=5)
        self.valor_var = tk.StringVar(value="0.00")
        tk.Entry(self, textvariable=self.valor_var, width=35).pack(pady=5)
        
        tk.Button(self, text="Guardar", command=self._guardar, bg='#4CAF50', fg='white',
                 font=('Arial', 10, 'bold'), padx=20, pady=8).pack(pady=20)
    
    def _guardar(self):
        from utils.helpers import obtener_categoria_desde_combo
        
        categoria = obtener_categoria_desde_combo(self.categoria_var.get())
        nombre = self.nombre_var.get().strip().upper()
        
        try:
            valor = float(self.valor_var.get())
            exito, mensaje = self.controller.agregar_cuenta(categoria, nombre, valor)
            
            if exito:
                self.cuenta_agregada = True
                messagebox.showinfo("Éxito", mensaje)
                self.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        except ValueError:
            messagebox.showerror("Error", "Valor inválido")
