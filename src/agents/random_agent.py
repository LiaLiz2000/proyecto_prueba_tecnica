"""
Agente con estrategia aleatoria
"""
#Imports
import random
from .base import Agent
from ..models import MarketState, Decision

class RandomAgent(Agent):
    """
    Agente con estrategia aleatoria(1/3 comprar, 1/3 vender, 1/3 hold)
    """
    def decide(self, market_state: MarketState, turn: int) -> Decision:
        """
        Decide random entre comprar, vender o no hacer nada
        market_state: Estado actual del mercado
        turn: Turno del agente en esta iteración
        
        Returns: 'buy', 'sell', o 'hold' con igual probabilidad
        """
        choice = random.random()
        if choice < 1/3:
            return 'buy'
        elif choice < 2/3:
            return 'sell'
        return 'hold'
