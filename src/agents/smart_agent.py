"""
Agente inteligente
"""
import random
from typing import List

from .base import Agent
from ..config import Config
from ..models import MarketState, Decision


class SmartAgent(Agent):
    """
    Agente inteligente con estrategia de fases:
    1 Acumulación (0-30%): Compra cuando precio bajo, construye posición
    2 Trading (30-70%): Trading activo (momentum y presión de mercado)
    3 Reducción (70-95%): Venta gradual con objetivos de ganancia
    4 Liquidación (95-100%): Venta total para cumplir requisito de 0 tarjetas

    (Adaptación temporal con estrategias por fase)
    """
    
    def __init__(self, agent_id: int):
        """
        Inicializa el SmartAgent con estado adicional
        """
        super().__init__(agent_id)
        self.price_history: List[float] = []
        self.avg_purchase_price: float = 0.0
        
        #Conocimiento del mercado (distribución de otros agentes)
        self.num_random = Config.NUM_RANDOM
        self.num_trend = Config.NUM_TREND
        self.num_anti_trend = Config.NUM_ANTI_TREND
    
    def _estimate_market_pressure(self, market_state: MarketState) -> float:
        """
        Estima la presión neta de compra/venta del mercado
        
        Analiza el comportamiento esperado de los otros agentes basándose
        en sus reglas conocidas y el cambio de precio actual
    
        Returns: Presión neta (positivo = compra, negativo = venta)
        """
        price_change = market_state.price_change_percentage()
        
        # Agentes aleatorios: neutral (1/3 compra - 1/3 venta = 0)
        random_pressure = 0
        
        # Agentes tendenciales
        if price_change >= 0.01:
            trend_pressure = self.num_trend * 0.75  # 75% compran
        else:
            trend_pressure = self.num_trend * -0.20  # 20% venden
        
        # Agentes anti-tendenciales
        if price_change <= -0.01:
            anti_trend_pressure = self.num_anti_trend * 0.75  # 75% compran
        else:
            anti_trend_pressure = self.num_anti_trend * -0.20  # 20% venden
        
        return random_pressure + trend_pressure + anti_trend_pressure
    
    def _calculate_momentum(self, window: int = 10) -> float: #Calcula el momentum del precio en las últimas N iteraciones
        """
        window: Tamaño de la ventana temporal
        Returns: Momentum (cambio porcentual en la ventana)float
        """
        if len(self.price_history) < window:
            return 0
        recent = self.price_history[-window:]
        return (recent[-1] - recent[0]) / recent[0]
    
    def _is_price_low(self, current_price: float, threshold: float = 0.97) -> bool: # Si el precio está bajo comparado con el promedio reciente

        if len(self.price_history) < 20:
            return current_price < Config.INITIAL_PRICE * 1.025
        
        avg_recent = sum(self.price_history[-20:]) / 20
        return current_price < avg_recent * threshold
    
    def _is_price_high(self, current_price: float, threshold: float = 1.03) -> bool: # Si el precio está alto comparado con el promedio reciente
        """
        current_price: Precio actual
        threshold: Umbral (ej: 1.03 = 3% sobre el promedio)
        True si el precio está alto
        """
        if len(self.price_history) < 20:
            return current_price > Config.INITIAL_PRICE * 1.10
        
        avg_recent = sum(self.price_history[-20:]) / 20
        return current_price > avg_recent * threshold
    
    def _calculate_reserve(self, iteration: int, total: int) -> float: # Calcula la reserva de efectivo a mantener
        """
        La reserva disminuye conforme avanza la simulación para permitir
        mayor inversión cuando nos acercamos al final 
        Returns: Cantidad a reservar
        """
        remaining_ratio = (total - iteration) / total
        return self.balance * (remaining_ratio ** 0.5) * 0.2
    
    def _update_avg_purchase_price(self, price: float): # Actualiza el precio promedio de compra
        """
        pass
        """
        if self.cards > 0:
            self.avg_purchase_price = (
                (self.avg_purchase_price * self.cards + price) / (self.cards + 1)
            )
        else:
            self.avg_purchase_price = price
    
    def decide(self, market_state: MarketState, turn: int) -> Decision:
        """
        Implementa la estrategia de 4 fases del agente inteligente.
        Returns:
            -Decision: 'buy', 'sell', o 'hold'
        """
        self.price_history.append(market_state.price)
        
        iteration = market_state.iteration
        total = market_state.total_iterations
        price = market_state.price
        
        # FASE 1: LIQUIDACIÓN TOTAL (últimas 50 iteraciones) =====
        if iteration >= total - 50:
            if self.cards > 0:
                return 'sell'
            return 'hold'
        
        # FASE 2: REDUCCIÓN GRADUAL (iteraciones 70%-95%) =====
        if iteration >= total * 0.7:
            if self.cards > 0:
                # Calcular target de tarjetas para esta iteración
                phase_progress = (iteration - total * 0.7) / (total * 0.25)
                target_cards = int(self.cards * (1 - phase_progress * 0.7))
                
                # Vender si tenemos más tarjetas del target y hay ganancia
                if self.cards > target_cards:
                    if self.avg_purchase_price > 0 and price >= self.avg_purchase_price * 1.03:
                        return 'sell'
                
                # O vender si estamos muy cerca del final
                if iteration >= total * 0.85 and random.random() < 0.4:
                    return 'sell'
            
            return 'hold'
        
        # FASE 3: TRADING ACTIVO (iteraciones 30%-70%) =====
        if iteration >= total * 0.3:
            market_pressure = self._estimate_market_pressure(market_state)
            momentum = self._calculate_momentum()
            
            # Vender si hay presión de compra fuerte y tenemos ganancias
            if market_pressure > 15 and self.cards > 0:
                if self.avg_purchase_price > 0 and price > self.avg_purchase_price * 1.08:
                    return 'sell'
            
            # Comprar si hay presión de venta y el precio es atractivo
            if market_pressure < -10 and self._is_price_low(price) and self.can_buy(price):
                reserve = self._calculate_reserve(iteration, total)
                if self.balance - price > reserve:
                    self._update_avg_purchase_price(price)
                    return 'buy'
            
            # Trading basado en momentum
            if momentum < -0.02 and self._is_price_low(price, 0.98) and self.can_buy(price):
                reserve = self._calculate_reserve(iteration, total)
                if self.balance - price > reserve:
                    self._update_avg_purchase_price(price)
                    return 'buy'
            
            return 'hold'
        
        # FASE 4: ACUMULACIÓN (iteraciones 0-30%) =====
        if self._is_price_low(price, 0.98) and self.can_buy(price):
            reserve = self._calculate_reserve(iteration, total)
            if self.balance - price > reserve:
                self._update_avg_purchase_price(price)
                return 'buy'
        
        return 'hold'
