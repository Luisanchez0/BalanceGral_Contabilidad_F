"""
utils/helpers.py
Funciones auxiliares y constantes
"""

from typing import Dict

# Constantes
TASA_IVA = 0.16

CATEGORIAS_NOMBRES = {
    'ACTIVO_CIRCULANTE': 'ACTIVO CIRCULANTE',
    'ACTIVO_NO_CIRCULANTE': 'ACTIVO NO CIRCULANTE',
    'PASIVO_LARGO_PLAZO': 'PASIVO LARGO PLAZO',
    'PASIVO_CORTO_PLAZO': 'PASIVO CORTO PLAZO',
    'CAPITAL': 'CAPITAL'
}

CATEGORIAS_COMBO = {
    'ACTIVO_CIRCULANTE': 'Activo Circulante',
    'ACTIVO_NO_CIRCULANTE': 'Activo No Circulante',
    'PASIVO_LARGO_PLAZO': 'Pasivo Largo Plazo',
    'PASIVO_CORTO_PLAZO': 'Pasivo Corto Plazo',
    'CAPITAL': 'Capital'
}

CUENTAS_PROTEGIDAS = ['CAJA', 'BANCO', 'CAPITAL SOCIAL']

# Colores
COLORES = {
    'primary': '#1976D2',
    'success': '#4CAF50',
    'warning': '#F57C00',
    'danger': '#D32F2F',
    'info': '#00796B',
    'dark': '#546E7A',
    'activo': '#BBDEFB',
    'pasivo': '#FFEBEE',
    'capital': '#E8F5E9',
    'highlight': '#FFF9C4',
    'total': '#81C784'
}


def formatear_moneda(valor: float) -> str:
    """Formatea un número como moneda"""
    return f"$ {valor:,.2f}"


def validar_numero(texto: str) -> bool:
    """Valida que un texto sea un número válido"""
    try:
        float(texto)
        return True
    except ValueError:
        return False


def obtener_categoria_desde_combo(valor_combo: str) -> str:
    """Convierte valor de combo a clave de categoría"""
    for key, val in CATEGORIAS_COMBO.items():
        if val == valor_combo:
            return key
    return None


def obtener_combo_desde_categoria(categoria: str) -> str:
    """Convierte clave de categoría a valor de combo"""
    return CATEGORIAS_COMBO.get(categoria, '')
