"""
main.py
Aplicación principal - Arquitectura MVC
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.balance_controller import BalanceController
from views.balance_view import BalanceView
from views.components.base_components import BotonAccion
from utils.helpers import COLORES


class BalanceApp:
    """Aplicación principal del Sistema de Balance General"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Balance General - LAVA TECH S.A de C.V")
        self.root.geometry("1400x900")
        
        # Inicializar controlador
        self.controller = BalanceController()
        
        # Configurar interfaz
        self.setup_ui()
        
        # Mostrar balance inicial
        self.mostrar_balance_inicial()
    
    def setup_ui(self):
        """Configura la interfaz principal"""
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        self._crear_titulo(main_frame)
        
        # Botones de transacciones
        self._crear_botones_transacciones(main_frame)
        
        # Botones de gestión
        self._crear_botones_gestion(main_frame)
        
        # Frame para el balance
        self.balance_frame = tk.Frame(main_frame)
        self.balance_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear vista del balance
        self.balance_view = BalanceView(self.balance_frame)
    
    def _crear_titulo(self, parent):
        """Crea el título de la aplicación"""
        title_frame = tk.Frame(parent, bg='#2E7D32')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(title_frame, text="LAVA TECH S.A de C.V",
                font=('Arial', 16, 'bold'), bg='#2E7D32', fg='white').pack(pady=5)
        tk.Label(title_frame, text="SISTEMA DE BALANCE GENERAL",
                font=('Arial', 12), bg='#2E7D32', fg='white').pack(pady=5)
    
    def _crear_botones_transacciones(self, parent):
        """Crea botones de transacciones"""
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(buttons_frame, text="Transacciones:",
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        transacciones = [
            ("1. Balance Inicial", self.mostrar_balance_inicial, 'primary'),
            ("2. Compra Efectivo", self.abrir_compra_efectivo, 'success'),
            ("3. Compra Crédito", self.abrir_compra_credito, 'warning'),
            ("4. Compra Combinada", self.abrir_compra_combinada, 'dark'),
            ("5. Anticipo Clientes", self.abrir_anticipo_clientes, 'info'),
        ]
        
        for texto, comando, color in transacciones:
            btn = tk.Button(buttons_frame, text=texto, command=comando,
                          bg=COLORES[color], fg='white', font=('Arial', 9, 'bold'),
                          padx=8, pady=5, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=2)
    
    def _crear_botones_gestion(self, parent):
        """Crea botones de gestión"""
        admin_frame = tk.Frame(parent)
        admin_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(admin_frame, text="Gestión:",
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        admin_buttons = [
            ("📋 Ver Catálogo", self.mostrar_catalogo, 'dark'),
            ("✏️ Editar Catálogo", self.editar_catalogo, 'info'),
            ("➕ Nueva Cuenta", self.agregar_cuenta, 'dark'),
            ("🔄 Reiniciar", self.reiniciar, 'danger')
        ]
        
        for texto, comando, color in admin_buttons:
            btn = tk.Button(admin_frame, text=texto, command=comando,
                          bg=COLORES[color], fg='white', font=('Arial', 9, 'bold'),
                          padx=8, pady=5, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=2)
    
    # === MÉTODOS DE VISUALIZACIÓN ===
    
    def mostrar_balance_inicial(self):
        """Muestra el balance general inicial"""
        estado = self.controller.obtener_estado_actual()
        totales = self.controller.calcular_totales()
        
        self.balance_view.mostrar_balance(
            estado,
            totales,
            "BALANCE GENERAL",
            None
        )
    
    def mostrar_balance_con_transaccion(self, detalles: dict):
        """Muestra el balance después de una transacción"""
        estado = self.controller.obtener_estado_actual()
        totales = self.controller.calcular_totales()
        
        tipo = detalles.get('tipo', '')
        descripcion = self._generar_descripcion_transaccion(detalles)
        
        self.balance_view.mostrar_balance(
            estado,
            totales,
            f"BALANCE GENERAL - {tipo}",
            descripcion,
            detalles
        )
    
    def _generar_descripcion_transaccion(self, detalles: dict) -> str:
        """Genera descripción de la transacción"""
        tipo = detalles.get('tipo', '')
        
        if tipo == 'COMPRA EFECTIVO':
            return f"Se pagó ${detalles['total']:,.2f} desde {detalles['cuenta_pago']} para aumentar {detalles['cuenta_destino']}"
        elif tipo == 'COMPRA CREDITO':
            return f"Pasivo registrado en: {detalles['cuenta_pasivo']}"
        elif tipo == 'COMPRA COMBINADA':
            return f"Pago: {detalles['cuenta_pago']} → Destino: {detalles['cuenta_destino']} → Crédito: {detalles['cuenta_pasivo']}"
        elif tipo == 'ANTICIPO CLIENTES':
            return f"Anticipo recibido en: {detalles['cuenta_recibe']}"
        
        return ""
    
    # === DIÁLOGOS DE TRANSACCIONES ===
    
    def abrir_compra_efectivo(self):
        """Abre diálogo para compra en efectivo"""
        from views.dialogs.transaccion_dialogs import DialogoCompraEfectivo
        
        dialog = DialogoCompraEfectivo(self.root, self.controller)
        self.root.wait_window(dialog)
        
        if dialog.resultado:
            exito, detalles, mensaje = dialog.resultado
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.mostrar_balance_con_transaccion(detalles)
            else:
                messagebox.showerror("Error", mensaje)
    
    def abrir_compra_credito(self):
        """Abre diálogo para compra a crédito"""
        from views.dialogs.transaccion_dialogs import DialogoCompraCredito
        
        dialog = DialogoCompraCredito(self.root, self.controller)
        self.root.wait_window(dialog)
        
        if dialog.resultado:
            exito, detalles, mensaje = dialog.resultado
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.mostrar_balance_con_transaccion(detalles)
            else:
                messagebox.showerror("Error", mensaje)
    
    def abrir_compra_combinada(self):
        """Abre diálogo para compra combinada"""
        from views.dialogs.transaccion_dialogs import DialogoCompraCombinada
        
        dialog = DialogoCompraCombinada(self.root, self.controller)
        self.root.wait_window(dialog)
        
        if dialog.resultado:
            exito, detalles, mensaje = dialog.resultado
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.mostrar_balance_con_transaccion(detalles)
            else:
                messagebox.showerror("Error", mensaje)
    
    def abrir_anticipo_clientes(self):
        """Abre diálogo para anticipo de clientes"""
        from views.dialogs.transaccion_dialogs import DialogoAnticipoClientes
        
        dialog = DialogoAnticipoClientes(self.root, self.controller)
        self.root.wait_window(dialog)
        
        if dialog.resultado:
            exito, detalles, mensaje = dialog.resultado
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.mostrar_balance_con_transaccion(detalles)
            else:
                messagebox.showerror("Error", mensaje)
    
    # === GESTIÓN DEL CATÁLOGO ===
    
    def mostrar_catalogo(self):
        """Muestra el catálogo completo"""
        from views.dialogs.catalogo_dialogs import DialogoCatalogo
        
        DialogoCatalogo(self.root, self.controller)
    
    def editar_catalogo(self):
        """Abre editor del catálogo"""
        from views.dialogs.catalogo_dialogs import DialogoEditarCatalogo
        
        dialog = DialogoEditarCatalogo(self.root, self.controller)
        self.root.wait_window(dialog)
        
        # Actualizar vista si hubo cambios
        if dialog.cambios_realizados:
            self.mostrar_balance_inicial()
    
    def agregar_cuenta(self):
        """Abre diálogo para agregar cuenta"""
        from views.dialogs.catalogo_dialogs import DialogoAgregarCuenta
        
        dialog = DialogoAgregarCuenta(self.root, self.controller)
        self.root.wait_window(dialog)
        
        if dialog.cuenta_agregada:
            self.mostrar_balance_inicial()
    
    def reiniciar(self):
        """Reinicia el sistema"""
        if messagebox.askyesno("Confirmar", "¿Desea reiniciar el sistema al estado inicial?"):
            exito, mensaje = self.controller.reiniciar_sistema()
            
            if exito:
                messagebox.showinfo("Reiniciar", mensaje)
                self.mostrar_balance_inicial()
            else:
                messagebox.showerror("Error", mensaje)


def main():
    """Función principal"""
    root = tk.Tk()
    app = BalanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
