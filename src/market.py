"""
Mercado de tarjetas gráficas ()gestion
"""
from typing import List

from .config import Config
from .models import MarketState


class Market:
    """
    El mercado mantiene el stock y ajusta el precio basándose
    en las transacciones de compra/venta realizadas por los agentes
    """
    
    def __init__(
        self,
        initial_price: float = Config.INITIAL_PRICE,
        initial_stock: int = Config.INITIAL_STOCK
    ):
       #inicializacion

        self.price = initial_price
        self.initial_price = initial_price
        self.stock = initial_stock
        self.previous_price = initial_price
        self.price_history: List[float] = [initial_price]
        self.volume_history: List[int] = []
    
    def apply_buy(self) -> bool:
        """
        Aplica el efecto de una compra en el mercado
        
        Una compra reduce el stock y aumenta el precio en 0.5%
        
        Returns:
        True si la compra fue exitosa (había stock), False en caso contrario
        """
        if self.stock > 0:
            self.stock -= 1
            self.price *= (1 + Config.PRICE_INCREASE_RATE)
            return True
        return False
    
    def apply_sell(self) -> bool:
        """
        Aplica el efecto de una venta en el mercado
        
        Una venta aumenta el stock y reduce el precio en 0.5%
        
        Returns: True (las ventas siempre son posibles)
        """
        self.stock += 1
        self.price *= (1 - Config.PRICE_DECREASE_RATE)
        return True
    
    def end_iteration(self):
        """
        Finaliza una iteración guardando el precio actual en el historial
        """
        self.price_history.append(self.price)
        self.previous_price = (
            self.price_history[-2] if len(self.price_history) > 1 
            else self.initial_price
        )
    
    def get_state(self, iteration: int, total_iterations: int) -> MarketState:
        """
        Obtiene el estado actual del mercado.
    
        """
        return MarketState(
            price=self.price,
            previous_price=self.previous_price,
            stock=self.stock,
            iteration=iteration,
            total_iterations=total_iterations
        )
    
    def get_statistics(self) -> dict:
        """
        Estadísticas del mercado.
        """
        return {
            'final_price': self.price,
            'initial_price': self.initial_price,
            'price_change_pct': ((self.price / self.initial_price) - 1) * 100,
            'final_stock': self.stock,
            'max_price': max(self.price_history),
            'min_price': min(self.price_history),
            'avg_price': sum(self.price_history) / len(self.price_history)
        }
