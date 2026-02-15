"""
views/components/base_components.py
Componentes reutilizables para las vistas
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional
from utils.helpers import COLORES, formatear_moneda


class FrameConScroll(tk.Frame):
    """Frame con scroll vertical"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Canvas y scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


class FilaCuenta(tk.Frame):
    """Fila para mostrar una cuenta con su valor"""
    
    def __init__(self, parent, nombre: str, valor: float, bg='white', **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.pack(fill=tk.X, padx=5, pady=1)
        
        tk.Label(self, text=nombre, font=('Arial', 9), bg=bg,
                anchor='w').pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(self, text=formatear_moneda(valor), font=('Arial', 9), bg=bg,
                anchor='e').pack(side=tk.RIGHT, padx=5)


class FilaTotal(tk.Frame):
    """Fila para mostrar un total"""
    
    def __init__(self, parent, nombre: str, valor: float, 
                bg='#FFF9C4', bold=False, **kwargs):
        super().__init__(parent, bg=bg, relief=tk.RIDGE, bd=1, **kwargs)
        self.pack(fill=tk.X, padx=5, pady=2)
        
        font = ('Arial', 10, 'bold') if bold else ('Arial', 9, 'bold')
        
        tk.Label(self, text=nombre, font=font, bg=bg,
                anchor='w').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Label(self, text=formatear_moneda(valor), font=font, bg=bg,
                anchor='e').pack(side=tk.RIGHT, padx=5)


class EncabezadoBalance(tk.Frame):
    """Encabezado estándar para balances"""
    
    def __init__(self, parent, titulo: str, subtitulo: str, 
                descripcion: Optional[str] = None, **kwargs):
        super().__init__(parent, bg=COLORES['capital'], relief=tk.RIDGE, bd=2, **kwargs)
        self.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(self, text=titulo, font=('Arial', 14, 'bold'),
                bg=COLORES['capital']).pack(pady=3)
        tk.Label(self, text=subtitulo, font=('Arial', 10),
                bg=COLORES['capital']).pack(pady=2)
        
        if descripcion:
            tk.Label(self, text=descripcion, font=('Arial', 9),
                    bg=COLORES['capital'], fg='#1565C0').pack(pady=2)


class PieBalance(tk.Frame):
    """Pie estándar para balances"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg='#F5F5F5', relief=tk.RIDGE, bd=1, **kwargs)
        self.pack(fill=tk.X, pady=(10, 0))
        
        pie_info = tk.Frame(self, bg='#F5F5F5')
        pie_info.pack(pady=10)
        
        tk.Label(pie_info, text="ELABORÓ:", font=('Arial', 9, 'bold'),
                bg='#F5F5F5').grid(row=0, column=0, padx=20, sticky='w')
        tk.Label(pie_info, text="LUIS MANUEL SANCHEZ GOMEZ", font=('Arial', 9),
                bg='#F5F5F5').grid(row=1, column=0, padx=20, sticky='w')
        
        tk.Label(pie_info, text="REVISÓ:", font=('Arial', 9, 'bold'),
                bg='#F5F5F5').grid(row=0, column=1, padx=20, sticky='w')
        tk.Label(pie_info, text="NURIA GONZALES ZUÑIGA", font=('Arial', 9),
                bg='#F5F5F5').grid(row=1, column=1, padx=20, sticky='w')


class DesgloseFactura(tk.Frame):
    """Frame para mostrar desglose de factura"""
    
    def __init__(self, parent, titulo: str, items: List[tuple], **kwargs):
        super().__init__(parent, relief=tk.RIDGE, bd=2, bg='#FFF8E1', **kwargs)
        self.pack(fill=tk.X, pady=10)
        
        tk.Label(self, text=titulo, font=('Arial', 11, 'bold'),
                bg='#FFF8E1').pack(pady=5)
        
        desglose = tk.Frame(self, bg='#FFF8E1')
        desglose.pack(pady=5)
        
        for label, valor, bold in items:
            font_style = ('Arial', 9, 'bold') if bold else ('Arial', 9)
            tk.Label(desglose, text=f"{label}: {formatear_moneda(valor)}",
                    font=font_style, bg='#FFF8E1').pack()


class BotonAccion(tk.Button):
    """Botón estilizado para acciones"""
    
    def __init__(self, parent, texto: str, comando: Callable,
                color: str = 'success', **kwargs):
        
        bg_color = COLORES.get(color, COLORES['primary'])
        
        super().__init__(
            parent,
            text=texto,
            command=comando,
            bg=bg_color,
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            **kwargs
        )


class SelectorCuenta(tk.Frame):
    """Componente para seleccionar una cuenta con tipo"""
    
    def __init__(self, parent, label: str, categorias: List[str],
                obtener_cuentas_callback: Callable, **kwargs):
        super().__init__(parent, **kwargs)
        
        tk.Label(self, text=label, font=('Arial', 11, 'bold')).pack(pady=5)
        
        # Tipo de cuenta (si hay múltiples categorías)
        if len(categorias) > 1:
            self.tipo_var = tk.StringVar(value=categorias[0])
            frame_tipo = tk.Frame(self)
            frame_tipo.pack(pady=5)
            
            for cat in categorias:
                tk.Radiobutton(
                    frame_tipo,
                    text=cat.replace('_', ' ').title(),
                    variable=self.tipo_var,
                    value=cat,
                    font=('Arial', 10)
                ).pack(side=tk.LEFT, padx=10)
        else:
            self.tipo_var = tk.StringVar(value=categorias[0])
        
        # Selector de cuenta
        self.cuenta_var = tk.StringVar()
        self.combo_cuenta = ttk.Combobox(
            self,
            textvariable=self.cuenta_var,
            state='readonly',
            width=30,
            font=('Arial', 10)
        )
        self.combo_cuenta.pack(pady=5)
        
        # Callback para actualizar cuentas
        self.obtener_cuentas = obtener_cuentas_callback
        
        # Actualizar cuando cambia el tipo
        if len(categorias) > 1:
            self.tipo_var.trace('w', self._actualizar_cuentas)
        
        self._actualizar_cuentas()
    
    def _actualizar_cuentas(self, *args):
        """Actualiza la lista de cuentas según el tipo seleccionado"""
        tipo = self.tipo_var.get()
        cuentas = self.obtener_cuentas(tipo)
        self.combo_cuenta['values'] = cuentas
        if cuentas:
            self.combo_cuenta.set(cuentas[0])
    
    def obtener_seleccion(self) -> tuple:
        """Retorna (tipo, cuenta)"""
        return self.tipo_var.get(), self.cuenta_var.get()


class CampoMoneda(tk.Frame):
    """Campo de entrada para montos"""
    
    def __init__(self, parent, label: str, valor_inicial: str = "0", **kwargs):
        super().__init__(parent, **kwargs)
        
        tk.Label(self, text=label, font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        self.valor_var = tk.StringVar(value=valor_inicial)
        self.entry = tk.Entry(
            self,
            textvariable=self.valor_var,
            font=('Arial', 10),
            width=15,
            justify='right'
        )
        self.entry.pack(side=tk.LEFT, padx=5)
    
    def obtener_valor(self) -> float:
        """Obtiene el valor como float"""
        try:
            return float(self.valor_var.get())
        except ValueError:
            return 0.0
    
    def establecer_valor(self, valor: float):
        """Establece un valor"""
        self.valor_var.set(f"{valor:.2f}")
