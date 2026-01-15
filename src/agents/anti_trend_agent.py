"""
Agente que va contra la tendencia del precio
"""
# Importaciones

import random
from .base import Agent
from ..models import MarketState, Decision


class AntiTrendAgent(Agent):
    """
    Agente anti-tendencial que va contra la tendencia del precio
    Precio baja ≥1%: 75% compra, 25% hold
    Si no: 20% vende
    Este agente compra en las caídas.
    """
    
    def decide(self, market_state: MarketState, turn: int) -> Decision:
        """
        Decide basándose en la contra-tendencia del precio.
        
        Compra agresivamente cuando detecta caída de precio (≥1%),
        y ocasionalmente vende cuando no hay caída significativa.
        
        Args:
            market_state: Estado actual del mercado
            turn: Turno del agente en esta iteración
        
        Returns:
            Decision: 'buy', 'sell', o 'hold'
        """
        price_change = market_state.price_change_percentage()
        
        if price_change <= -0.01:  # Precio bajó 1% o más
            return 'buy' if random.random() < 0.75 else 'hold'
        else:
            return 'sell' if random.random() < 0.20 else 'hold'
