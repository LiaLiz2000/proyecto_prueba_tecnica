"""
Modelos de datos para la simulación
"""

from dataclasses import dataclass
from typing import Literal


# Tipo para las decisiones de los agentes
Decision = Literal['buy', 'sell', 'hold']


@dataclass
class MarketState:
    """
    Estado inmutable del mercado en un momento dado.

    price: Precio actual de las tarjetas
    previous_price: Precio en la iteración anterior
    stock: Cantidad de tarjetas disponibles
    iteration: Número de iteración actual
    total_iterations: Total de iteraciones de la simulación
    """
    price: float
    previous_price: float
    stock: int
    iteration: int
    total_iterations: int
    
    def price_change_percentage(self) -> float:
        """
        Calcula el cambio porcentual del precio.
        Returns: Cambio porcentual (ej: 0.01 = 1% de aumento)
        """
        if self.previous_price == 0:
            return 0
        return (self.price - self.previous_price) / self.previous_price
