"""
views/balance_view.py
Vista principal del balance general
"""

import tkinter as tk
from datetime import datetime
from typing import Dict
from views.components.base_components import (
    FrameConScroll, FilaCuenta, FilaTotal, 
    EncabezadoBalance, PieBalance, DesgloseFactura
)
from utils.helpers import COLORES


class BalanceView:
    """Vista para mostrar el balance general"""
    
    def __init__(self, parent: tk.Frame):
        self.parent = parent
    
    def limpiar(self):
        """Limpia el frame"""
        for widget in self.parent.winfo_children():
            widget.destroy()
    
    def mostrar_balance(self, estado: Dict, totales: Dict, 
                       titulo: str = "BALANCE GENERAL",
                       descripcion: str = None,
                       desglose: Dict = None):
        """
        Muestra el balance general completo
        
        Args:
            estado: Estado actual de las cuentas
            totales: Totales calculados
            titulo: Título del balance
            descripcion: Descripción adicional
            desglose: Desglose de factura (opcional)
        """
        self.limpiar()
        
        # Frame con scroll
        scroll_frame = FrameConScroll(self.parent)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Usar el scrollable_frame interno
        frame = scroll_frame.scrollable_frame
        
        # Encabezado
        fecha = datetime.now().strftime('%d de %B %Y')
        EncabezadoBalance(
            frame,
            titulo,
            f"ESTADO DE SITUACION FINANCIERA {fecha}",
            descripcion
        )
        
        # Frame principal para activo y pasivo
        main_balance = tk.Frame(frame)
        main_balance.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # ACTIVO
        activo_frame = tk.Frame(main_balance, relief=tk.GROOVE, bd=2)
        activo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(activo_frame, text="ACTIVO", font=('Arial', 12, 'bold'),
                bg=COLORES['activo']).pack(fill=tk.X)
        
        # Activo Circulante
        tk.Label(activo_frame, text="CIRCULANTE", font=('Arial', 10, 'bold'),
                bg='#E3F2FD', anchor='w').pack(fill=tk.X, padx=5, pady=2)
        
        for cuenta, valor in estado['ACTIVO_CIRCULANTE'].items():
            FilaCuenta(activo_frame, cuenta, valor)
        
        FilaTotal(activo_frame, "SUMA ACTIVOS CIRC.", 
                 totales['activo_circulante'], bg=COLORES['highlight'])
        
        # Activo No Circulante
        tk.Label(activo_frame, text="NO CIRCULANTE", font=('Arial', 10, 'bold'),
                bg='#E3F2FD', anchor='w').pack(fill=tk.X, padx=5, pady=2)
        
        for cuenta, valor in estado['ACTIVO_NO_CIRCULANTE'].items():
            FilaCuenta(activo_frame, cuenta, valor)
        
        FilaTotal(activo_frame, "SUMA ACTIVOS", 
                 totales['activo_no_circulante'], bg=COLORES['highlight'])
        
        FilaTotal(activo_frame, "TOTAL", totales['total_activo'], 
                 bg=COLORES['total'], bold=True)
        
        # PASIVO Y CAPITAL
        pasivo_frame = tk.Frame(main_balance, relief=tk.GROOVE, bd=2)
        pasivo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(pasivo_frame, text="CAPITAL CONTABLE", font=('Arial', 12, 'bold'),
                bg=COLORES['activo']).pack(fill=tk.X)
        
        # Pasivo Largo Plazo
        if totales['pasivo_largo_plazo'] > 0:
            tk.Label(pasivo_frame, text="PASIVO", font=('Arial', 10, 'bold'),
                    bg=COLORES['pasivo'], anchor='w').pack(fill=tk.X, padx=5, pady=2)
            tk.Label(pasivo_frame, text="LARGO PLAZO", font=('Arial', 9, 'bold'),
                    bg='#FCE4EC', anchor='w').pack(fill=tk.X, padx=10, pady=1)
            
            for cuenta, valor in estado['PASIVO_LARGO_PLAZO'].items():
                if valor > 0:
                    FilaCuenta(pasivo_frame, cuenta, valor)
        
        # Pasivo Corto Plazo
        if totales['pasivo_corto_plazo'] > 0:
            if totales['pasivo_largo_plazo'] == 0:
                tk.Label(pasivo_frame, text="PASIVO", font=('Arial', 10, 'bold'),
                        bg=COLORES['pasivo'], anchor='w').pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(pasivo_frame, text="CORTO PLAZO", font=('Arial', 9, 'bold'),
                    bg='#FCE4EC', anchor='w').pack(fill=tk.X, padx=10, pady=1)
            
            for cuenta, valor in estado['PASIVO_CORTO_PLAZO'].items():
                if valor > 0:
                    FilaCuenta(pasivo_frame, cuenta, valor)
        
        if totales['pasivo_largo_plazo'] > 0 or totales['pasivo_corto_plazo'] > 0:
            tk.Label(pasivo_frame, text="", height=1).pack()
        
        # Capital
        for cuenta, valor in estado['CAPITAL'].items():
            FilaCuenta(pasivo_frame, cuenta, valor)
        
        tk.Label(pasivo_frame, text="", height=2).pack()
        
        FilaTotal(pasivo_frame, "TOTAL", totales['total_pasivo_capital'],
                 bg=COLORES['total'], bold=True)
        
        # Verificar balance
        if not totales['balance_cuadra']:
            warning_frame = tk.Frame(frame, bg='#FFEBEE', relief=tk.RIDGE, bd=2)
            warning_frame.pack(fill=tk.X, pady=5)
            tk.Label(
                warning_frame,
                text=f"⚠️ ADVERTENCIA: El balance no cuadra. Diferencia: ${totales['diferencia']:,.2f}",
                font=('Arial', 10, 'bold'),
                bg='#FFEBEE',
                fg='red'
            ).pack(pady=5)
        
        # Desglose si existe
        if desglose:
            self._mostrar_desglose(frame, desglose)
        
        # Pie
        PieBalance(frame)
    
    def _mostrar_desglose(self, parent, desglose: Dict):
        """Muestra el desglose de una transacción"""
        tipo = desglose.get('tipo', '')
        
        if tipo == 'COMPRA EFECTIVO' or tipo == 'COMPRA COMBINADA':
            items = [
                ("SUBTOTAL", desglose.get('subtotal', 0), False),
                ("IVA (16%)", desglose.get('iva_total', desglose.get('iva', 0)), False),
                ("TOTAL", desglose.get('total', 0), True)
            ]
            
            DesgloseFactura(parent, "DESGLOCE DE FACTURA", items)
            
            # Si es combinada, mostrar anticipo y deuda
            if tipo == 'COMPRA COMBINADA':
                # Anticipo
                items_anticipo = [
                    ("SUBTOTAL", desglose.get('sub_anticipo', 0), False),
                    ("IVA ACREDITABLE", desglose.get('iva_anticipo', 0), False),
                    ("TOTAL", desglose.get('anticipo', 0), True)
                ]
                
                titulo_anticipo = f"ANTICIPO {desglose.get('porcentaje_anticipo', 0):.0f}% ({desglose.get('cuenta_pago', '')})"
                DesgloseFactura(parent, titulo_anticipo, items_anticipo)
                
                # Deuda
                items_deuda = [
                    ("SUBTOTAL", desglose.get('sub_deuda', 0), False),
                    ("IVA X ACREDITAR", desglose.get('iva_deuda', 0), False),
                    ("TOTAL", desglose.get('deuda', 0), True)
                ]
                
                porc_deuda = 100 - desglose.get('porcentaje_anticipo', 0)
                titulo_deuda = f"DEUDA {porc_deuda:.0f}% ({desglose.get('cuenta_pasivo', '')})"
                DesgloseFactura(parent, titulo_deuda, items_deuda)
        
        elif tipo == 'COMPRA CREDITO':
            # Múltiples conceptos
            detalles = desglose.get('detalles', [])
            
            for detalle in detalles:
                items = [
                    ("SUBTOTAL", detalle.get('subtotal', 0), False),
                    ("IVA", detalle.get('iva', 0), False),
                    ("TOTAL", detalle.get('total', 0), True)
                ]
                
                titulo = detalle.get('cuenta', 'CONCEPTO')
                DesgloseFactura(parent, titulo, items)
            
            # Totales
            frame_totales = tk.Frame(parent, bg='#FFF8E1', relief=tk.RIDGE, bd=2)
            frame_totales.pack(fill=tk.X, pady=5)
            
            tk.Label(frame_totales, text=f"SUMA IVA: ${desglose.get('total_iva', 0):,.2f}",
                    font=('Arial', 10, 'bold'), bg='#FFF8E1', fg='red').pack(pady=2)
            tk.Label(frame_totales, text=f"TOTAL CRÉDITO: ${desglose.get('total_credito', 0):,.2f}",
                    font=('Arial', 10, 'bold'), bg='#FFF8E1', fg='blue').pack(pady=2)
        
        elif tipo == 'ANTICIPO CLIENTES':
            # Venta total
            items_venta = [
                ("SUBTOTAL", desglose.get('subtotal', 0), False),
                ("IVA", desglose.get('iva_total', 0), False),
                ("TOTAL", desglose.get('total_venta', 0), True)
            ]
            DesgloseFactura(parent, "VENTA TOTAL", items_venta)
            
            # Anticipo recibido
            items_anticipo = [
                ("SUBTOTAL", desglose.get('sub_anticipo', 0), False),
                ("IVA", desglose.get('iva_anticipo', 0), False),
                ("TOTAL", desglose.get('anticipo', 0), True)
            ]
            
            titulo = f"{desglose.get('porcentaje_anticipo', 0):.0f}% ANTICIPO RECIBIDO"
            DesgloseFactura(parent, titulo, items_anticipo)
