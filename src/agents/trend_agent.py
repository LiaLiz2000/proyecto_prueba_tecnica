"""
Agente que sigue la tendencia del precio
"""

import random

from .base import Agent
from ..models import MarketState, Decision


class TrendAgent(Agent):
    """
    Agente que sigue la tendencia del precio.
    
    Comportamiento:
    - Si el precio sube ≥1%: 75% compra, 25% hold
    - Si no: 20% vende, 80% hold
    
    Este agente amplifica los movimientos alcistas del mercado.
    """
    
    def decide(self, market_state: MarketState, turn: int) -> Decision:
        """
        Decide basándose en la tendencia del precio.
        Compra cuando detecta subida de precio (≥1%),
        y ocasionalmente vende cuando no hay tendencia alcista.
        Returns: 'buy', 'sell', o 'hold'
        """
        price_change = market_state.price_change_percentage()
        
        if price_change >= 0.01:  # Precio subió 1% o más
            return 'buy' if random.random() < 0.75 else 'hold'
        else:
            return 'sell' if random.random() < 0.20 else 'hold'
