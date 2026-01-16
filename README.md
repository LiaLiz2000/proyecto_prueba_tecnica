# Simulación de Mercado de Tarjetas Gráficas

## Objetivo

Desarrollar una simulación de mercado en Python con múltiples agentes que compran y venden tarjetas gráficas siguiendo distintas estrategias.

El objetivo principal es implementar un **SmartAgent** que maximice su balance tras 1.000 iteraciones y finalice la simulación sin tarjetas en su posesión.

---

## Solución

La solución implementa un sistema multiagente basado en programación orientada a objetos.  
Cada agente toma decisiones de compra, venta o espera en función del estado del mercado en cada iteración.

El sistema está diseñado para ser:

- Modular  
- Fácil de mantener  
- Fácil de extender  
- Totalmente testeable  

---

## Estructura del proyecto

```text
proyecto/
├── src/
│   ├── config.py          # Configuración y validaciones
│   ├── models.py          # Estados y tipos de datos
│   ├── market.py          # Lógica de precios y transacciones
│   ├── simulation.py     # Control de la simulación
│   └── agents/            # Estrategias de agentes
│       ├── base.py
│       ├── random_agent.py
│       ├── trend_agent.py
│       ├── anti_trend_agent.py
│       └── smart_agent.py
├── tests/
├── main.py
└── run_multiple_simulations.py



Resultados
El SmartAgent obtiene beneficios de forma consistente y finaliza siempre la simulación sin tarjetas en su poder, cumpliendo los requisitos planteados en la prueba.
