# Balance General - Arquitectura MVC

## 📁 Estructura del Proyecto

```
balance_app/
│
├── main.py                          # Punto de entrada de la aplicación
│
├── models/                          # MODELO - Lógica de negocio
│   ├── __init__.py
│   └── balance_model.py            # Modelo de datos y cálculos
│
├── views/                           # VISTA - Interfaz de usuario
│   ├── __init__.py
│   ├── balance_view.py             # Vista principal del balance
│   ├── components/                 # Componentes reutilizables
│   │   ├── __init__.py
│   │   └── base_components.py     # Widgets personalizados
│   └── dialogs/                    # Diálogos/ventanas modales
│       ├── __init__.py
│       ├── transaccion_dialogs.py # Diálogos de transacciones
│       └── catalogo_dialogs.py    # Diálogos de catálogo
│
├── controllers/                     # CONTROLADOR - Lógica de control
│   ├── __init__.py
│   └── balance_controller.py      # Controlador principal
│
└── utils/                          # UTILIDADES
    ├── __init__.py
    └── helpers.py                  # Funciones auxiliares y constantes
```

## 🏗️ Arquitectura MVC (Model-View-Controller)

### 📊 MODEL (Modelo)
**Archivo:** `models/balance_model.py`

**Responsabilidad:** Maneja la lógica de negocio y los datos

**Contiene:**
- Estructura del catálogo de cuentas
- Estado actual del balance
- Cálculos financieros (IVA, totales, etc.)
- Operaciones CRUD sobre cuentas
- Lógica de transacciones contables

**Métodos principales:**
```python
- agregar_cuenta()
- modificar_cuenta()
- eliminar_cuenta()
- calcular_iva()
- calcular_totales()
- compra_efectivo()
- compra_credito()
- compra_combinada()
- anticipo_clientes()
```

**Ventajas:**
- ✅ No depende de la interfaz gráfica
- ✅ Se puede probar independientemente
- ✅ Reutilizable en otros proyectos
- ✅ Cambios en la UI no afectan la lógica

---

### 🎨 VIEW (Vista)
**Archivos:** `views/` y sus subdirectorios

**Responsabilidad:** Presentación visual de los datos

**Componentes:**

#### 1. `balance_view.py`
- Muestra el balance general completo
- Renderiza activos, pasivos y capital
- Muestra desgloses de transacciones
- Actualiza la visualización

#### 2. `components/base_components.py`
Componentes reutilizables:
- `FrameConScroll` - Frame con scroll vertical
- `FilaCuenta` - Fila para mostrar cuenta y valor
- `FilaTotal` - Fila para totales
- `EncabezadoBalance` - Encabezado estándar
- `PieBalance` - Pie con firmas
- `DesgloseFactura` - Desglose de IVA
- `BotonAccion` - Botón estilizado
- `SelectorCuenta` - Selector de cuenta con tipo
- `CampoMoneda` - Campo para montos

#### 3. `dialogs/transaccion_dialogs.py`
Diálogos para transacciones:
- `DialogoCompraEfectivo`
- `DialogoCompraCredito`
- `DialogoCompraCombinada`
- `DialogoAnticipoClientes`

#### 4. `dialogs/catalogo_dialogs.py`
Diálogos para catálogo:
- `DialogoCatalogo` - Ver catálogo
- `DialogoEditarCatalogo` - Editar valores
- `DialogoAgregarCuenta` - Nueva cuenta

**Ventajas:**
- ✅ Componentes reutilizables
- ✅ Fácil de modificar el diseño
- ✅ No contiene lógica de negocio
- ✅ Código organizado por función

---

### 🎮 CONTROLLER (Controlador)
**Archivo:** `controllers/balance_controller.py`

**Responsabilidad:** Coordina el Modelo y la Vista

**Funciones:**
- Recibe eventos de la Vista
- Invoca métodos del Modelo
- Valida datos de entrada
- Maneja errores
- Retorna resultados a la Vista

**Métodos principales:**
```python
# Gestión de catálogo
- agregar_cuenta()
- modificar_cuenta()
- eliminar_cuenta()
- obtener_cuentas()
- obtener_catalogo_completo()

# Cálculos
- calcular_totales()
- calcular_iva()

# Validaciones
- validar_fondos()
- verificar_balance_cuadrado()

# Transacciones
- realizar_compra_efectivo()
- realizar_compra_credito()
- realizar_compra_combinada()
- realizar_anticipo_clientes()

# Sistema
- reiniciar_sistema()
- exportar_estado_completo()
```

**Ventajas:**
- ✅ Separa la lógica de presentación y negocio
- ✅ Valida antes de enviar al modelo
- ✅ Maneja errores centralizadamente
- ✅ Facilita el testing

---

### 🛠️ UTILS (Utilidades)
**Archivo:** `utils/helpers.py`

**Responsabilidad:** Funciones y constantes compartidas

**Contiene:**
- Constantes (colores, tasas, nombres)
- Funciones de formateo
- Funciones de validación
- Conversiones

---

## 🔄 Flujo de Datos

```
┌─────────────┐
│    VISTA    │ ◄─── El usuario interactúa con la interfaz
└──────┬──────┘
       │ 1. Evento (ej: clic en "Compra Efectivo")
       ▼
┌──────────────┐
│ CONTROLADOR  │ ◄─── Recibe el evento
└──────┬───────┘
       │ 2. Valida datos
       │ 3. Invoca método del modelo
       ▼
┌─────────────┐
│   MODELO    │ ◄─── Ejecuta lógica de negocio
└──────┬──────┘
       │ 4. Retorna resultado
       ▼
┌──────────────┐
│ CONTROLADOR  │ ◄─── Procesa resultado
└──────┬───────┘
       │ 5. Actualiza vista
       ▼
┌─────────────┐
│    VISTA    │ ◄─── Muestra resultado al usuario
└─────────────┘
```

---

## 💡 Ejemplo Práctico: Compra en Efectivo

### 1. Usuario hace clic en "Compra Efectivo"
```python
# main.py (Vista Principal)
def abrir_compra_efectivo(self):
    dialog = DialogoCompraEfectivo(self.root, self.controller)
    # ...
```

### 2. Usuario llena el formulario y da clic en "Aplicar"
```python
# views/dialogs/transaccion_dialogs.py
def _aplicar(self):
    cuenta_pago = self.cuenta_pago_var.get()
    tipo_dest, cuenta_dest = self.selector_destino.obtener_seleccion()
    total = self.campo_monto.obtener_valor()
    
    # Llamar al controlador
    self.resultado = self.controller.realizar_compra_efectivo(
        cuenta_pago, tipo_dest, cuenta_dest, total
    )
```

### 3. Controlador valida y procesa
```python
# controllers/balance_controller.py
def realizar_compra_efectivo(self, cuenta_pago, tipo_destino, cuenta_destino, total):
    # Validar fondos
    tiene_fondos, msg = self.validar_fondos(cuenta_pago, total)
    
    if not tiene_fondos:
        return False, {}, msg
    
    # Llamar al modelo
    detalles = self.modelo.compra_efectivo(
        cuenta_pago, tipo_destino, cuenta_destino, total
    )
    
    return True, detalles, "Transacción exitosa"
```

### 4. Modelo ejecuta la transacción
```python
# models/balance_model.py
def compra_efectivo(self, cuenta_pago, tipo_destino, cuenta_destino, total):
    subtotal, iva = self.calcular_iva(total, incluye_iva=True)
    
    # Actualizar cuentas
    self.estado_actual['ACTIVO_CIRCULANTE'][cuenta_pago] -= total
    self.estado_actual[tipo_destino][cuenta_destino] += subtotal
    self.estado_actual['ACTIVO_CIRCULANTE']['IVA ACREDITABLE'] += iva
    
    return {'tipo': 'COMPRA EFECTIVO', 'total': total, ...}
```

### 5. Vista actualiza el balance
```python
# main.py
if exito:
    self.mostrar_balance_con_transaccion(detalles)
```

---

## 🎯 Ventajas de esta Arquitectura

### ✅ Separación de Responsabilidades
- Cada capa tiene una función específica
- Cambios en una capa no afectan las otras
- Código más limpio y mantenible

### ✅ Reutilización de Código
- Componentes visuales reutilizables
- Lógica de negocio independiente
- Utilidades compartidas

### ✅ Facilidad de Testing
```python
# Se puede probar el modelo sin GUI
def test_compra_efectivo():
    modelo = BalanceModel()
    resultado = modelo.compra_efectivo('BANCO', 'ACTIVO_CIRCULANTE', 'INVENTARIO', 1000)
    assert resultado['total'] == 1000
```

### ✅ Escalabilidad
- Fácil agregar nuevas transacciones
- Fácil agregar nuevas vistas
- Fácil modificar la lógica de negocio

### ✅ Mantenibilidad
- Código organizado y estructurado
- Fácil encontrar y corregir errores
- Documentación clara

---

## 🚀 Cómo Ejecutar

```bash
cd balance_app
python main.py
```

---

## 📝 Cómo Extender

### Agregar una Nueva Transacción

#### 1. Agregar método en el Modelo
```python
# models/balance_model.py
def nueva_transaccion(self, param1, param2):
    # Lógica de la transacción
    return detalles
```

#### 2. Agregar método en el Controlador
```python
# controllers/balance_controller.py
def realizar_nueva_transaccion(self, param1, param2):
    # Validaciones
    detalles = self.modelo.nueva_transaccion(param1, param2)
    return exito, detalles, mensaje
```

#### 3. Crear Diálogo en la Vista
```python
# views/dialogs/transaccion_dialogs.py
class DialogoNuevaTransaccion(tk.Toplevel):
    def __init__(self, parent, controller):
        # Crear interfaz
        pass
```

#### 4. Conectar en main.py
```python
# main.py
def abrir_nueva_transaccion(self):
    dialog = DialogoNuevaTransaccion(self.root, self.controller)
    # ...
```

---

## 🔍 Comparación: Monolítico vs MVC

### ❌ Código Monolítico (1 archivo, 2000+ líneas)
```
- Difícil de mantener
- Difícil de probar
- Difícil de colaborar
- Cambios arriesgados
- Código duplicado
```

### ✅ Arquitectura MVC (múltiples archivos, organizados)
```
- Fácil de mantener
- Fácil de probar cada parte
- Múltiples personas pueden trabajar
- Cambios seguros y localizados
- Código reutilizable
```

---

## 📚 Recursos

- **Python Tkinter:** https://docs.python.org/3/library/tkinter.html
- **MVC Pattern:** https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
- **Clean Code:** Robert C. Martin

---

## 👨‍💻 Autor
**Luis Manuel Sanchez Gomez**

## 📅 Versión
**3.0 - Arquitectura MVC** (Febrero 2026)

---

**¡Arquitectura profesional para aplicaciones profesionales!** 🚀
