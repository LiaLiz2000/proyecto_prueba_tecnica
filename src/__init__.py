"""
Paquete principal del sistema de simulación de mercado
"""

from .config import Config
from .models import MarketState, Decision
from .market import Market
from .simulation import Simulation
from .agents import (
    Agent,
    RandomAgent,
    TrendAgent,
    AntiTrendAgent,
    SmartAgent
)
__version__ = '1.0.0'

__all__ = [
    'Config',
    'MarketState',
    'Decision',
    'Market',
    'Simulation',
    'Agent',
    'RandomAgent',
    'TrendAgent',
    'AntiTrendAgent',
    'SmartAgent',
]
