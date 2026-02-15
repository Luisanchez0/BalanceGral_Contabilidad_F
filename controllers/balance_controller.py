"""
controllers/balance_controller.py
Controlador principal - Maneja la lógica entre el modelo y las vistas
"""

from typing import Dict, List, Tuple, Optional
from models.balance_model import BalanceModel


class BalanceController:
    """Controlador que coordina el modelo y las vistas"""
    
    def __init__(self):
        self.modelo = BalanceModel()
    
    # === OPERACIONES DE CATÁLOGO ===
    
    def agregar_cuenta(self, categoria: str, nombre: str, valor: float) -> Tuple[bool, str]:
        """
        Agrega una nueva cuenta al catálogo
        
        Returns:
            Tuple (éxito, mensaje)
        """
        if not nombre:
            return False, "El nombre de la cuenta no puede estar vacío"
        
        nombre = nombre.strip().upper()
        
        if self.modelo.agregar_cuenta(categoria, nombre, valor):
            return True, f"Cuenta '{nombre}' agregada exitosamente"
        else:
            return False, f"La cuenta '{nombre}' ya existe en esta categoría"
    
    def modificar_cuenta(self, categoria: str, nombre: str, nuevo_valor: float) -> Tuple[bool, str]:
        """
        Modifica el valor de una cuenta
        
        Returns:
            Tuple (éxito, mensaje)
        """
        if self.modelo.modificar_cuenta(categoria, nombre, nuevo_valor):
            return True, f"Cuenta '{nombre}' actualizada"
        else:
            return False, f"No se pudo actualizar la cuenta '{nombre}'"
    
    def eliminar_cuenta(self, categoria: str, nombre: str) -> Tuple[bool, str]:
        """
        Elimina una cuenta del catálogo
        
        Returns:
            Tuple (éxito, mensaje)
        """
        if self.modelo.eliminar_cuenta(categoria, nombre):
            return True, f"Cuenta '{nombre}' eliminada"
        else:
            return False, f"No se puede eliminar la cuenta '{nombre}' (es una cuenta protegida)"
    
    def obtener_cuentas(self, categoria: str) -> List[str]:
        """Obtiene lista de cuentas de una categoría"""
        return self.modelo.obtener_cuentas(categoria)
    
    def obtener_catalogo_completo(self) -> Dict:
        """Obtiene el catálogo completo"""
        return self.modelo.catalogo
    
    def obtener_estado_actual(self) -> Dict:
        """Obtiene el estado actual de todas las cuentas"""
        return self.modelo.estado_actual
    
    # === CÁLCULOS ===
    
    def calcular_totales(self) -> Dict[str, float]:
        """Calcula los totales del balance"""
        return self.modelo.calcular_totales()
    
    def calcular_iva(self, monto: float, incluye_iva: bool = False) -> Tuple[float, float]:
        """Calcula el IVA de un monto"""
        return self.modelo.calcular_iva(monto, incluye_iva)
    
    # === VALIDACIONES ===
    
    def validar_fondos(self, cuenta: str, monto: float) -> Tuple[bool, str]:
        """
        Valida si una cuenta tiene fondos suficientes
        
        Returns:
            Tuple (tiene_fondos, mensaje)
        """
        fondos = self.modelo.obtener_valor_cuenta('ACTIVO_CIRCULANTE', cuenta)
        
        if fondos >= monto:
            return True, "Fondos suficientes"
        else:
            faltante = monto - fondos
            return False, f"Fondos insuficientes. Faltan: ${faltante:,.2f}"
    
    def verificar_balance_cuadrado(self) -> Tuple[bool, float]:
        """
        Verifica si el balance está cuadrado
        
        Returns:
            Tuple (cuadra, diferencia)
        """
        totales = self.modelo.calcular_totales()
        return totales['balance_cuadra'], totales['diferencia']
    
    # === TRANSACCIONES ===
    
    def realizar_compra_efectivo(self, cuenta_pago: str, tipo_destino: str,
                                cuenta_destino: str, total: float,
                                forzar: bool = False) -> Tuple[bool, Dict, str]:
        """
        Realiza una compra en efectivo
        
        Returns:
            Tuple (éxito, detalles, mensaje)
        """
        try:
            # Validar fondos
            tiene_fondos, msg_fondos = self.validar_fondos(cuenta_pago, total)
            
            if not tiene_fondos and not forzar:
                return False, {}, msg_fondos
            
            # Realizar transacción
            detalles = self.modelo.compra_efectivo(cuenta_pago, tipo_destino, 
                                                   cuenta_destino, total)
            
            return True, detalles, "Transacción realizada exitosamente"
            
        except KeyError as e:
            return False, {}, f"Cuenta no encontrada: {e}"
        except Exception as e:
            return False, {}, f"Error al realizar la transacción: {e}"
    
    def realizar_compra_credito(self, compras: List[Tuple[str, str, float]],
                               tipo_pasivo: str, cuenta_pasivo: str) -> Tuple[bool, Dict, str]:
        """
        Realiza una compra a crédito
        
        Returns:
            Tuple (éxito, detalles, mensaje)
        """
        try:
            if not compras:
                return False, {}, "Debe agregar al menos un concepto"
            
            # Realizar transacción
            detalles = self.modelo.compra_credito(compras, tipo_pasivo, cuenta_pasivo)
            
            return True, detalles, "Compra a crédito realizada exitosamente"
            
        except KeyError as e:
            return False, {}, f"Cuenta no encontrada: {e}"
        except Exception as e:
            return False, {}, f"Error al realizar la transacción: {e}"
    
    def realizar_compra_combinada(self, cuenta_pago: str, tipo_destino: str,
                                 cuenta_destino: str, tipo_pasivo: str,
                                 cuenta_pasivo: str, total: float,
                                 porcentaje_anticipo: float,
                                 forzar: bool = False) -> Tuple[bool, Dict, str]:
        """
        Realiza una compra combinada
        
        Returns:
            Tuple (éxito, detalles, mensaje)
        """
        try:
            anticipo = total * porcentaje_anticipo
            
            # Validar fondos para el anticipo
            tiene_fondos, msg_fondos = self.validar_fondos(cuenta_pago, anticipo)
            
            if not tiene_fondos and not forzar:
                return False, {}, f"Fondos insuficientes para el anticipo. {msg_fondos}"
            
            # Realizar transacción
            detalles = self.modelo.compra_combinada(
                cuenta_pago, tipo_destino, cuenta_destino,
                tipo_pasivo, cuenta_pasivo, total, porcentaje_anticipo
            )
            
            return True, detalles, "Compra combinada realizada exitosamente"
            
        except KeyError as e:
            return False, {}, f"Cuenta no encontrada: {e}"
        except Exception as e:
            return False, {}, f"Error al realizar la transacción: {e}"
    
    def realizar_anticipo_clientes(self, cuenta_recibe: str, total_venta: float,
                                  porcentaje_anticipo: float) -> Tuple[bool, Dict, str]:
        """
        Registra un anticipo de clientes
        
        Returns:
            Tuple (éxito, detalles, mensaje)
        """
        try:
            # Realizar transacción
            detalles = self.modelo.anticipo_clientes(
                cuenta_recibe, total_venta, porcentaje_anticipo
            )
            
            return True, detalles, "Anticipo de clientes registrado exitosamente"
            
        except KeyError as e:
            return False, {}, f"Cuenta no encontrada: {e}"
        except Exception as e:
            return False, {}, f"Error al realizar la transacción: {e}"
    
    def reiniciar_sistema(self) -> Tuple[bool, str]:
        """
        Reinicia el sistema al estado inicial
        
        Returns:
            Tuple (éxito, mensaje)
        """
        try:
            self.modelo.reiniciar()
            return True, "Sistema reiniciado al estado inicial"
        except Exception as e:
            return False, f"Error al reiniciar: {e}"
    
    # === EXPORTACIÓN ===
    
    def exportar_estado_completo(self) -> Dict:
        """Exporta el estado completo del sistema"""
        return self.modelo.exportar_estado()
