"""
models/balance_model.py
Modelo de datos para el Balance General - Maneja la lógica de negocio
"""

import copy
from typing import Dict, List, Tuple, Optional


class BalanceModel:
    """Modelo que contiene la lógica de negocio del Balance General"""
    
    def __init__(self):
        # Catálogo de cuentas editable
        self.catalogo = {
            'ACTIVO_CIRCULANTE': {
                'CAJA': 50000.00,
                'BANCO': 2000000.00,
                'INVENTARIO': 800000.00,
                'PAPELERIA': 50000.00,
                'RENTA': 130000.00,
                'IVA ACREDITABLE': 0.00,
                'IVA POR ACREDITAR': 0.00
            },
            'ACTIVO_NO_CIRCULANTE': {
                'TERRENOS': 4000000.00,
                'EDIFICIOS': 12000000.00,
                'MOBILIARIA Y EQUIPO': 700000.00,
                'EQ. COMPUTO': 600000.00,
                'EQ. ENTREGA': 1500000.00,
                'GAST. CONSTITUCION': 120000.00,
                'GAST. INST': 300000.00
            },
            'PASIVO_LARGO_PLAZO': {
                'HIPOTECAS': 0.00,
                'DOCUMENTOS POR PAGAR LP': 0.00
            },
            'PASIVO_CORTO_PLAZO': {
                'ACREEDORES': 0.00,
                'PROVEEDORES': 0.00,
                'DOCUMENTOS POR PAGAR CP': 0.00
            },
            'CAPITAL': {
                'CAPITAL SOCIAL': 22250000.00,
                'ANTICIPO CLIENTES': 0.00,
                'IVA TRASLADO': 0.00,
                'GANADO': 0.00,
                'UTILIDAD': 0.00,
                'PERDIDA': 0.00
            }
        }
        
        self.estado_actual = self._copiar_catalogo()
        self.estado_inicial = self._copiar_catalogo()
        
        # Tasa de IVA
        self.tasa_iva = 0.16
    
    def _copiar_catalogo(self) -> Dict:
        """Crea una copia profunda del catálogo"""
        return {
            categoria: dict(cuentas)
            for categoria, cuentas in self.catalogo.items()
        }
    
    # === OPERACIONES DE CATÁLOGO ===
    
    def agregar_cuenta(self, categoria: str, nombre: str, valor: float) -> bool:
        """Agrega una nueva cuenta al catálogo"""
        if nombre in self.catalogo[categoria]:
            return False
        
        self.catalogo[categoria][nombre] = valor
        self.estado_actual[categoria][nombre] = valor
        self.estado_inicial[categoria][nombre] = valor
        return True
    
    def modificar_cuenta(self, categoria: str, nombre: str, nuevo_valor: float) -> bool:
        """Modifica el valor de una cuenta en el catálogo"""
        if nombre not in self.catalogo[categoria]:
            return False
        
        self.catalogo[categoria][nombre] = nuevo_valor
        self.estado_inicial[categoria][nombre] = nuevo_valor
        return True
    
    def eliminar_cuenta(self, categoria: str, nombre: str) -> bool:
        """Elimina una cuenta del catálogo (si no es básica)"""
        cuentas_protegidas = ['CAJA', 'BANCO', 'CAPITAL SOCIAL']
        
        if nombre in cuentas_protegidas:
            return False
        
        if nombre in self.catalogo[categoria]:
            del self.catalogo[categoria][nombre]
            if nombre in self.estado_actual[categoria]:
                del self.estado_actual[categoria][nombre]
            if nombre in self.estado_inicial[categoria]:
                del self.estado_inicial[categoria][nombre]
            return True
        
        return False
    
    def obtener_cuentas(self, categoria: str) -> List[str]:
        """Obtiene lista de cuentas de una categoría"""
        return list(self.catalogo[categoria].keys())
    
    def obtener_valor_cuenta(self, categoria: str, cuenta: str) -> float:
        """Obtiene el valor actual de una cuenta"""
        return self.estado_actual[categoria].get(cuenta, 0.0)
    
    # === CÁLCULOS FINANCIEROS ===
    
    def calcular_iva(self, monto: float, incluye_iva: bool = False) -> Tuple[float, float]:
        """
        Calcula el IVA de un monto
        
        Args:
            monto: Monto total
            incluye_iva: Si True, el monto ya incluye IVA
        
        Returns:
            Tuple (subtotal, iva)
        """
        if incluye_iva:
            subtotal = monto / (1 + self.tasa_iva)
            iva = monto - subtotal
        else:
            subtotal = monto
            iva = monto * self.tasa_iva
        
        return subtotal, iva
    
    def calcular_totales(self) -> Dict[str, float]:
        """Calcula los totales del balance"""
        suma_circulante = sum(self.estado_actual['ACTIVO_CIRCULANTE'].values())
        suma_no_circulante = sum(self.estado_actual['ACTIVO_NO_CIRCULANTE'].values())
        total_activo = suma_circulante + suma_no_circulante
        
        suma_pasivo_lp = sum(self.estado_actual['PASIVO_LARGO_PLAZO'].values())
        suma_pasivo_cp = sum(self.estado_actual['PASIVO_CORTO_PLAZO'].values())
        suma_capital = sum(self.estado_actual['CAPITAL'].values())
        total_pasivo_capital = suma_pasivo_lp + suma_pasivo_cp + suma_capital
        
        diferencia = abs(total_activo - total_pasivo_capital)
        
        return {
            'activo_circulante': suma_circulante,
            'activo_no_circulante': suma_no_circulante,
            'total_activo': total_activo,
            'pasivo_largo_plazo': suma_pasivo_lp,
            'pasivo_corto_plazo': suma_pasivo_cp,
            'capital': suma_capital,
            'total_pasivo_capital': total_pasivo_capital,
            'diferencia': diferencia,
            'balance_cuadra': diferencia <= 0.01
        }
    
    # === TRANSACCIONES ===
    
    def compra_efectivo(self, cuenta_pago: str, tipo_destino: str, 
                       cuenta_destino: str, total: float) -> Dict:
        """
        Realiza una compra en efectivo
        
        Returns:
            Dict con detalles de la transacción
        """
        subtotal, iva = self.calcular_iva(total, incluye_iva=True)
        
        # Verificar fondos
        fondos_disponibles = self.estado_actual['ACTIVO_CIRCULANTE'][cuenta_pago]
        tiene_fondos = fondos_disponibles >= total
        
        # Actualizar cuentas
        self.estado_actual['ACTIVO_CIRCULANTE'][cuenta_pago] -= total
        self.estado_actual[tipo_destino][cuenta_destino] += subtotal
        self.estado_actual['ACTIVO_CIRCULANTE']['IVA ACREDITABLE'] += iva
        
        return {
            'tipo': 'COMPRA EFECTIVO',
            'cuenta_pago': cuenta_pago,
            'cuenta_destino': cuenta_destino,
            'total': total,
            'subtotal': subtotal,
            'iva': iva,
            'tiene_fondos': tiene_fondos
        }
    
    def compra_credito(self, compras: List[Tuple[str, str, float]], 
                      tipo_pasivo: str, cuenta_pasivo: str) -> Dict:
        """
        Realiza una compra a crédito con múltiples conceptos
        
        Args:
            compras: Lista de (tipo_activo, cuenta, total)
            tipo_pasivo: Categoría del pasivo
            cuenta_pasivo: Cuenta de pasivo
        
        Returns:
            Dict con detalles de la transacción
        """
        total_credito = 0
        total_iva = 0
        detalles = []
        
        for tipo_activo, cuenta, total in compras:
            subtotal, iva = self.calcular_iva(total, incluye_iva=True)
            
            # Actualizar activo
            self.estado_actual[tipo_activo][cuenta] += subtotal
            total_iva += iva
            total_credito += total
            
            detalles.append({
                'cuenta': cuenta,
                'total': total,
                'subtotal': subtotal,
                'iva': iva
            })
        
        # Actualizar IVA y pasivo
        self.estado_actual['ACTIVO_CIRCULANTE']['IVA POR ACREDITAR'] += total_iva
        self.estado_actual[tipo_pasivo][cuenta_pasivo] += total_credito
        
        return {
            'tipo': 'COMPRA CREDITO',
            'detalles': detalles,
            'total_credito': total_credito,
            'total_iva': total_iva,
            'cuenta_pasivo': cuenta_pasivo
        }
    
    def compra_combinada(self, cuenta_pago: str, tipo_destino: str,
                        cuenta_destino: str, tipo_pasivo: str,
                        cuenta_pasivo: str, total: float, 
                        porcentaje_anticipo: float) -> Dict:
        """
        Realiza una compra combinada (anticipo + crédito)
        
        Returns:
            Dict con detalles de la transacción
        """
        subtotal, iva_total = self.calcular_iva(total, incluye_iva=True)
        
        # Calcular anticipo y deuda
        anticipo = total * porcentaje_anticipo
        deuda = total - anticipo
        
        sub_anticipo, iva_anticipo = self.calcular_iva(anticipo, incluye_iva=True)
        sub_deuda, iva_deuda = self.calcular_iva(deuda, incluye_iva=True)
        
        # Actualizar cuentas
        self.estado_actual['ACTIVO_CIRCULANTE'][cuenta_pago] -= anticipo
        self.estado_actual[tipo_destino][cuenta_destino] += subtotal
        self.estado_actual['ACTIVO_CIRCULANTE']['IVA ACREDITABLE'] += iva_anticipo
        self.estado_actual['ACTIVO_CIRCULANTE']['IVA POR ACREDITAR'] += iva_deuda
        self.estado_actual[tipo_pasivo][cuenta_pasivo] += deuda
        
        return {
            'tipo': 'COMPRA COMBINADA',
            'cuenta_pago': cuenta_pago,
            'cuenta_destino': cuenta_destino,
            'cuenta_pasivo': cuenta_pasivo,
            'total': total,
            'subtotal': subtotal,
            'iva_total': iva_total,
            'anticipo': anticipo,
            'sub_anticipo': sub_anticipo,
            'iva_anticipo': iva_anticipo,
            'deuda': deuda,
            'sub_deuda': sub_deuda,
            'iva_deuda': iva_deuda,
            'porcentaje_anticipo': porcentaje_anticipo * 100
        }
    
    def anticipo_clientes(self, cuenta_recibe: str, total_venta: float,
                         porcentaje_anticipo: float) -> Dict:
        """
        Registra un anticipo de clientes
        
        Returns:
            Dict con detalles de la transacción
        """
        subtotal, iva_total = self.calcular_iva(total_venta, incluye_iva=True)
        
        anticipo = total_venta * porcentaje_anticipo
        sub_anticipo, iva_anticipo = self.calcular_iva(anticipo, incluye_iva=True)
        
        # Actualizar cuentas
        self.estado_actual['ACTIVO_CIRCULANTE'][cuenta_recibe] += anticipo
        
        # Crear o actualizar cuentas de anticipo
        if 'ANTICIPO CLIENTES' in self.estado_actual['CAPITAL']:
            self.estado_actual['CAPITAL']['ANTICIPO CLIENTES'] += sub_anticipo
        else:
            self.estado_actual['CAPITAL']['ANTICIPO CLIENTES'] = sub_anticipo
        
        if 'IVA TRASLADO' in self.estado_actual['CAPITAL']:
            self.estado_actual['CAPITAL']['IVA TRASLADO'] += iva_anticipo
        else:
            self.estado_actual['CAPITAL']['IVA TRASLADO'] = iva_anticipo
        
        return {
            'tipo': 'ANTICIPO CLIENTES',
            'cuenta_recibe': cuenta_recibe,
            'total_venta': total_venta,
            'subtotal': subtotal,
            'iva_total': iva_total,
            'anticipo': anticipo,
            'sub_anticipo': sub_anticipo,
            'iva_anticipo': iva_anticipo,
            'porcentaje_anticipo': porcentaje_anticipo * 100
        }
    
    def reiniciar(self):
        """Reinicia el estado al inicial"""
        self.estado_actual = self._copiar_catalogo()
    
    def exportar_estado(self) -> Dict:
        """Exporta el estado actual completo"""
        return {
            'catalogo': self.catalogo,
            'estado_actual': self.estado_actual,
            'totales': self.calcular_totales()
        }
