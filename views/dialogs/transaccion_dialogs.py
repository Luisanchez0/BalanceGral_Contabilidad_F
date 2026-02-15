"""
views/dialogs/transaccion_dialogs.py
Diálogos para transacciones
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_components import BotonAccion, SelectorCuenta, CampoMoneda


class DialogoCompraEfectivo(tk.Toplevel):
    """Diálogo para compra en efectivo"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.resultado = None
        
        self.title("Compra en Efectivo")
        self.geometry("500x400")
        self.transient(parent)
        self.grab_set()
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        tk.Label(self, text="Compra en Efectivo", font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Cuenta de pago
        tk.Label(self, text="1. Cuenta de pago:", font=('Arial', 11, 'bold')).pack(pady=5)
        self.cuenta_pago_var = tk.StringVar()
        combo = ttk.Combobox(self, textvariable=self.cuenta_pago_var, state='readonly', width=30)
        combo['values'] = self.controller.obtener_cuentas('ACTIVO_CIRCULANTE')
        combo.set('BANCO' if 'BANCO' in combo['values'] else combo['values'][0] if combo['values'] else '')
        combo.pack(pady=5)
        
        # Selector de destino
        self.selector_destino = SelectorCuenta(
            self, "2. Cuenta destino:",
            ['ACTIVO_CIRCULANTE', 'ACTIVO_NO_CIRCULANTE'],
            self.controller.obtener_cuentas
        )
        self.selector_destino.pack(pady=10)
        
        # Monto
        self.campo_monto = CampoMoneda(self, "3. Monto total (con IVA):", "400000")
        self.campo_monto.pack(pady=10)
        
        BotonAccion(self, "✓ Aplicar", self._aplicar, 'success').pack(pady=20)
    
    def _aplicar(self):
        try:
            cuenta_pago = self.cuenta_pago_var.get()
            tipo_dest, cuenta_dest = self.selector_destino.obtener_seleccion()
            total = self.campo_monto.obtener_valor()
            
            self.resultado = self.controller.realizar_compra_efectivo(
                cuenta_pago, tipo_dest, cuenta_dest, total, forzar=True
            )
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class DialogoCompraCredito(tk.Toplevel):
    """Diálogo para compra a crédito"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.resultado = None
        self.compras = []
        
        self.title("Compra a Crédito")
        self.geometry("600x500")
        self.transient(parent)
        self.grab_set()
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        tk.Label(self, text="Compra a Crédito", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para compras
        self.frame_compras = tk.Frame(self)
        self.frame_compras.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botón agregar
        tk.Button(self, text="➕ Agregar Concepto", command=self._agregar_compra).pack()
        
        # Tipo de pasivo
        tk.Label(self, text="Tipo de pasivo:", font=('Arial', 10, 'bold')).pack()
        self.pasivo_tipo_var = tk.StringVar(value='PASIVO_LARGO_PLAZO')
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Radiobutton(frame, text="Largo Plazo", variable=self.pasivo_tipo_var,
                      value='PASIVO_LARGO_PLAZO').pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame, text="Corto Plazo", variable=self.pasivo_tipo_var,
                      value='PASIVO_CORTO_PLAZO').pack(side=tk.LEFT, padx=10)
        
        self.cuenta_pasivo_var = tk.StringVar()
        self.combo_pasivo = ttk.Combobox(self, textvariable=self.cuenta_pasivo_var,
                                        state='readonly', width=25)
        self.combo_pasivo.pack(pady=5)
        self.pasivo_tipo_var.trace('w', self._actualizar_pasivo)
        self._actualizar_pasivo()
        
        BotonAccion(self, "✓ Aplicar", self._aplicar, 'success').pack(pady=10)
        
        # Agregar primera compra
        self._agregar_compra()
    
    def _agregar_compra(self):
        frame = tk.Frame(self.frame_compras, relief=tk.RIDGE, bd=2, bg='#E3F2FD')
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tipo_var = tk.StringVar(value='ACTIVO_NO_CIRCULANTE')
        cuenta_var = tk.StringVar()
        monto_var = tk.StringVar(value="0")
        
        tk.Radiobutton(frame, text="Circ.", variable=tipo_var, value='ACTIVO_CIRCULANTE',
                      bg='#E3F2FD').pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="No Circ.", variable=tipo_var, value='ACTIVO_NO_CIRCULANTE',
                      bg='#E3F2FD').pack(side=tk.LEFT)
        
        combo = ttk.Combobox(frame, textvariable=cuenta_var, state='readonly', width=20)
        combo.pack(side=tk.LEFT, padx=5)
        
        tk.Entry(frame, textvariable=monto_var, width=12).pack(side=tk.LEFT, padx=5)
        
        def actualizar(*args):
            combo['values'] = self.controller.obtener_cuentas(tipo_var.get())
            if combo['values']:
                combo.set(combo['values'][0])
        
        tipo_var.trace('w', actualizar)
        actualizar()
        
        self.compras.append((tipo_var, cuenta_var, monto_var, frame))
    
    def _actualizar_pasivo(self, *args):
        tipo = self.pasivo_tipo_var.get()
        cuentas = self.controller.obtener_cuentas(tipo)
        self.combo_pasivo['values'] = cuentas
        if cuentas:
            self.combo_pasivo.set(cuentas[0])
    
    def _aplicar(self):
        try:
            compras_list = []
            for tipo_var, cuenta_var, monto_var, frame in self.compras:
                total = float(monto_var.get())
                if total > 0:
                    compras_list.append((tipo_var.get(), cuenta_var.get(), total))
            
            tipo_pasivo = self.pasivo_tipo_var.get()
            cuenta_pasivo = self.cuenta_pasivo_var.get()
            
            self.resultado = self.controller.realizar_compra_credito(
                compras_list, tipo_pasivo, cuenta_pasivo
            )
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class DialogoCompraCombinada(tk.Toplevel):
    """Diálogo para compra combinada"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.resultado = None
        
        self.title("Compra Combinada")
        self.geometry("500x450")
        self.transient(parent)
        self.grab_set()
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        tk.Label(self, text="Compra Combinada", font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Selectores similares a DialogoCompraEfectivo
        self.selector_pago = SelectorCuenta(
            self, "1. Cuenta de pago (anticipo):",
            ['ACTIVO_CIRCULANTE'],
            self.controller.obtener_cuentas
        )
        self.selector_pago.pack(pady=5)
        
        self.selector_destino = SelectorCuenta(
            self, "2. Cuenta destino:",
            ['ACTIVO_CIRCULANTE', 'ACTIVO_NO_CIRCULANTE'],
            self.controller.obtener_cuentas
        )
        self.selector_destino.pack(pady=5)
        
        self.selector_pasivo = SelectorCuenta(
            self, "3. Cuenta de pasivo (crédito):",
            ['PASIVO_CORTO_PLAZO', 'PASIVO_LARGO_PLAZO'],
            self.controller.obtener_cuentas
        )
        self.selector_pasivo.pack(pady=5)
        
        # Montos
        frame_montos = tk.Frame(self)
        frame_montos.pack(pady=10)
        
        self.campo_total = CampoMoneda(frame_montos, "Total (con IVA):", "500000")
        self.campo_total.pack()
        
        self.campo_anticipo = CampoMoneda(frame_montos, "% Anticipo:", "40")
        self.campo_anticipo.pack()
        
        BotonAccion(self, "✓ Aplicar", self._aplicar, 'success').pack(pady=20)
    
    def _aplicar(self):
        try:
            _, cuenta_pago = self.selector_pago.obtener_seleccion()
            tipo_dest, cuenta_dest = self.selector_destino.obtener_seleccion()
            tipo_pas, cuenta_pas = self.selector_pasivo.obtener_seleccion()
            total = self.campo_total.obtener_valor()
            porc = self.campo_anticipo.obtener_valor() / 100
            
            self.resultado = self.controller.realizar_compra_combinada(
                cuenta_pago, tipo_dest, cuenta_dest, tipo_pas, cuenta_pas, total, porc, True
            )
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class DialogoAnticipoClientes(tk.Toplevel):
    """Diálogo para anticipo de clientes"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.resultado = None
        
        self.title("Anticipo de Clientes")
        self.geometry("500x300")
        self.transient(parent)
        self.grab_set()
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        tk.Label(self, text="Anticipo de Clientes", font=('Arial', 14, 'bold')).pack(pady=20)
        
        self.selector_recibe = SelectorCuenta(
            self, "1. Cuenta que recibe:",
            ['ACTIVO_CIRCULANTE'],
            self.controller.obtener_cuentas
        )
        self.selector_recibe.pack(pady=10)
        
        frame_montos = tk.Frame(self)
        frame_montos.pack(pady=10)
        
        self.campo_total = CampoMoneda(frame_montos, "Total venta (con IVA):", "339990")
        self.campo_total.pack()
        
        self.campo_anticipo = CampoMoneda(frame_montos, "% Anticipo:", "40")
        self.campo_anticipo.pack()
        
        BotonAccion(self, "✓ Aplicar", self._aplicar, 'success').pack(pady=20)
    
    def _aplicar(self):
        try:
            _, cuenta_recibe = self.selector_recibe.obtener_seleccion()
            total = self.campo_total.obtener_valor()
            porc = self.campo_anticipo.obtener_valor() / 100
            
            self.resultado = self.controller.realizar_anticipo_clientes(
                cuenta_recibe, total, porc
            )
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
