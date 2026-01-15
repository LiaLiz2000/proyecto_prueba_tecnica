"""
Clase base abstracta para todos los agentes del mercado
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

from ..config import Config
from ..models import MarketState, Decision


class Agent(ABC):
    """
    Los agentes TODOS heredan de esta clase e implementan el método
    decide() con su estrategia específica.
    """
    
    def __init__(self, agent_id: int):
    
        self.agent_id = agent_id #identificador
        self.balance: float = Config.INITIAL_BALANCE
        self.cards: int = 0
        self.transactions: List[Tuple[str, float, int]] = []
    
    @abstractmethod
    def decide(self, market_state: MarketState, turn: int) -> Decision:# decide qué hacer
        """
            market_state: Estado actual del mercado
            turn: Turno del agente en esta iteración (0-99)
            Decision: ¿'buy', 'sell', o 'hold'?
        """
        pass
    
    def can_buy(self, price: float) -> bool: #Verifica si el agente tiene fondos suficientes para comprar
        """
        price: Precio actual de una tarjeta
        Returns: True si puede comprar, False en caso contrario
        """
        return self.balance >= price
    
    def can_sell(self) -> bool: #Verifica si tiene tarjetas para vender
        """
        Returns: True si tiene tarjetas, False en caso contrario
        """
        return self.cards > 0
    
    def buy(self, price: float, iteration: int) -> bool:# Ejecuta una compra
        
        if self.can_buy(price):
            self.balance -= price
            self.cards += 1
            self.transactions.append(('buy', price, iteration))
            return True
        return False
    
    def sell(self, price: float, iteration: int) -> bool: # Ejecuta una venta
        if self.can_sell():
            self.balance += price
            self.cards -= 1
            self.transactions.append(('sell', price, iteration))
            return True
        return False
    
    def get_total_value(self, current_price: float) -> float: # Calcula el valor total del agente
        """
        (balance + valor de tarjetas)
        current_price: Precio actual de las tarjetas
        
        Returns: Valor total del agente
        """
        return self.balance + (self.cards * current_price)
    
    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.agent_id}, "
                f"balance=${self.balance:.2f}, cards={self.cards})")
