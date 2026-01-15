"""
Configuración global del sistema de simulación
"""
class Config:
    """Configuración centralizada de la simulación"""
    
    # Balance y mercado inicial
    INITIAL_BALANCE: float = 1000.0
    INITIAL_STOCK: int = 100000
    INITIAL_PRICE: float = 200.0
    
    # Dinámica de precios
    PRICE_INCREASE_RATE: float = 0.005  # 0.5% por compra
    PRICE_DECREASE_RATE: float = 0.005  # 0.5% por venta
    
    # Configuración de simulación
    TOTAL_ITERATIONS: int = 1000
    
    # Distribución de agentes
    NUM_RANDOM: int = 51
    NUM_TREND: int = 24
    NUM_ANTI_TREND: int = 24
    NUM_SMART: int = 1
    
    @classmethod
    def validate(cls):
        """Valida que la configuración sea correcta"""
        total = cls.NUM_RANDOM + cls.NUM_TREND + cls.NUM_ANTI_TREND + cls.NUM_SMART
        if total != 100:
            raise ValueError(f"El total de agentes debe ser 100, actual: {total}")
        
        if cls.TOTAL_ITERATIONS <= 0:
            raise ValueError("El número de iteraciones debe ser positivo")
        
        if any([
            cls.NUM_RANDOM < 0,
            cls.NUM_TREND < 0,
            cls.NUM_ANTI_TREND < 0,
            cls.NUM_SMART < 0
        ]):
            raise ValueError("El número de agentes no puede ser negativo")
