# Simulación de Mercado de Tarjetas Gráficas

## Descripción

Simulación de un mercado económico donde 100 agentes con diferentes estrategias compran y venden tarjetas gráficas. El objetivo es implementar un agente inteligente que maximice su balance tras 1.000 iteraciones y finalice con 0 tarjetas en su posesión.

---

## Inicio Rápido

### Requisitos
- Python 3.8 o superior
- No requiere dependencias externas

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/LiaLiz2000/proyecto_prueba_tecnica.git


# Ejecutar simulación
python3 main.py

# Ejecutar tests
python3 tests/test_simulation.py
```

---

## Estructura del Proyecto
```
proyecto/
├── src/
│   ├── config.py              # Configuración centralizada
│   ├── models.py              # Modelos de datos (MarketState, Decision)
│   ├── market.py              # Lógica del mercado y precios
│   ├── simulation.py          # Orquestación de la simulación
│   └── agents/                # Paquete de agentes
│       ├── base.py            # Clase base abstracta
│       ├── random_agent.py    # Agente aleatorio
│       ├── trend_agent.py     # Agente tendencial
│       ├── anti_trend_agent.py # Agente anti-tendencial
│       └── smart_agent.py     # Agente inteligente
├── tests/
│   └── test_simulation.py     # 38 tests unitarios
├── main.py                    # Punto de entrada
└── run_multiple_simulations.py # Análisis estadístico (opcional)
```

---

## Uso

### Ejecutar Simulación Principal
```bash
python3 main.py
```

**Salida esperada:**
```
============================================================
SIMULACIÓN DEL MERCADO DE TARJETAS GRÁFICAS
============================================================
Precio inicial: $200.00
...
El agente terminó con 0 tarjetas (requisito cumplido)
```

### Ejecutar Tests
```bash
python3 tests/test_simulation.py
```

**Salida esperada:**
```
Ran 38 tests in 0.XXXs
OK
```

## Estrategia del SmartAgent

El SmartAgent implementa una estrategia adaptativa dividida en 4 fases:

### Fase 1: Acumulación (0-30%)
Compra cuando el precio está bajo (<98% del promedio reciente) manteniendo reservas de efectivo.

### Fase 2: Trading Activo (30-70%)
- Estima presión de mercado basándose en comportamiento de otros agentes
- Vende con ganancias cuando hay presión de compra
- Compra oportunista cuando hay momentum negativo

### Fase 3: Reducción Gradual (70-95%)
Liquida posiciones progresivamente priorizando ventas con >3% de ganancia.

### Fase 4: Liquidación Total (95-100%)
Vende todas las tarjetas restantes para cumplir el requisito de 0 tarjetas al final.

**Ventaja competitiva**: El SmartAgent conoce la distribución de agentes (51 aleatorios, 24 tendenciales, 24 anti-tendenciales) y usa esta información para predecir movimientos del mercado.

---

## Resultados

El SmartAgent obtiene consistentemente:
- Balance final: $1,150 - $1,350 (15%-35% de ganancia)
- Ranking: Top 1-5 de 100 agentes (90%+ de las veces)
- Tarjetas finales: 0 (100% de cumplimiento)
- Transacciones: 50-100 operaciones optimizadas

---

## Arquitectura

### Principios Aplicados

- **POO**: Herencia, abstracción (ABC), polimorfismo
- **SOLID**: Single Responsibility, Open/Closed, Dependency Inversion
- **Clean Code**: Type hints completos, nombres descriptivos, funciones focalizadas
- **Modularidad**: Alta cohesión dentro de módulos, bajo acoplamiento entre ellos


## Tests

El proyecto incluye 38 tests unitarios que validan:

- Configuración del sistema
- Lógica de agentes (compra, venta, balance)
- Dinámica del mercado (precios, stock)
- Decisiones de cada tipo de agente
- Integración completa (SmartAgent termina con 0 tarjetas)

**Cobertura**: 100% de funcionalidades críticas

---

## Configuración

Para modificar parámetros de la simulación, edita `src/config.py`:
```python
class Config:
    INITIAL_BALANCE: float = 1000.0    # Balance inicial
    INITIAL_PRICE: float = 200.0       # Precio inicial
    TOTAL_ITERATIONS: int = 1000       # Iteraciones
    NUM_RANDOM: int = 51               # Agentes aleatorios
    NUM_TREND: int = 24                # Agentes tendenciales
    NUM_ANTI_TREND: int = 24           # Agentes anti-tendenciales
    NUM_SMART: int = 1                 # Agentes inteligentes
```

