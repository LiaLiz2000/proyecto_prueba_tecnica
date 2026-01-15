"""
Tests Unitarios para el Sistema de Simulación
Ejecutar con: python -m pytest tests/test_simulation.py -v
O simplemente: python tests/test_simulation.py
"""

import sys
import os
# Agregar el directorio raíz al path para importar src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src import (
    Config, MarketState, Market, Simulation,
    Agent, RandomAgent, TrendAgent, AntiTrendAgent, SmartAgent
)


class TestConfig(unittest.TestCase):
    """Tests para la configuración del sistema"""
    
    def test_config_validation_success(self):
        """Test que la configuración por defecto es válida"""
        try:
            Config.validate()
        except ValueError:
            self.fail("La configuración por defecto debería ser válida")
    
    def test_total_agents_is_100(self):
        """Test que el total de agentes suma 100"""
        total = Config.NUM_RANDOM + Config.NUM_TREND + Config.NUM_ANTI_TREND + Config.NUM_SMART
        self.assertEqual(total, 100)


class TestAgent(unittest.TestCase):
    """Tests para la clase base Agent y sus métodos comunes"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.agent = RandomAgent(agent_id=1)
    
    def test_initial_balance(self):
        """Test que el balance inicial es correcto"""
        self.assertEqual(self.agent.balance, Config.INITIAL_BALANCE)
    
    def test_initial_cards(self):
        """Test que inicia sin tarjetas"""
        self.assertEqual(self.agent.cards, 0)
    
    def test_can_buy_with_sufficient_funds(self):
        """Test que puede comprar si tiene fondos suficientes"""
        self.assertTrue(self.agent.can_buy(Config.INITIAL_PRICE))
    
    def test_cannot_buy_without_sufficient_funds(self):
        """Test que no puede comprar sin fondos suficientes"""
        self.agent.balance = 50.0
        self.assertFalse(self.agent.can_buy(100.0))
    
    def test_cannot_sell_without_cards(self):
        """Test que no puede vender sin tarjetas"""
        self.assertEqual(self.agent.cards, 0)
        self.assertFalse(self.agent.can_sell())
    
    def test_can_sell_with_cards(self):
        """Test que puede vender si tiene tarjetas"""
        self.agent.cards = 1
        self.assertTrue(self.agent.can_sell())
    
    def test_successful_buy(self):
        """Test de compra exitosa"""
        initial_balance = self.agent.balance
        price = 200.0
        result = self.agent.buy(price, iteration=0)
        
        self.assertTrue(result)
        self.assertEqual(self.agent.balance, initial_balance - price)
        self.assertEqual(self.agent.cards, 1)
        self.assertEqual(len(self.agent.transactions), 1)
        self.assertEqual(self.agent.transactions[0][0], 'buy')
    
    def test_failed_buy_insufficient_funds(self):
        """Test de compra fallida por fondos insuficientes"""
        self.agent.balance = 50.0
        result = self.agent.buy(100.0, iteration=0)
        
        self.assertFalse(result)
        self.assertEqual(self.agent.balance, 50.0)
        self.assertEqual(self.agent.cards, 0)
    
    def test_successful_sell(self):
        """Test de venta exitosa"""
        self.agent.cards = 1
        initial_balance = self.agent.balance
        price = 200.0
        result = self.agent.sell(price, iteration=0)
        
        self.assertTrue(result)
        self.assertEqual(self.agent.balance, initial_balance + price)
        self.assertEqual(self.agent.cards, 0)
        self.assertEqual(len(self.agent.transactions), 1)
        self.assertEqual(self.agent.transactions[0][0], 'sell')
    
    def test_failed_sell_no_cards(self):
        """Test de venta fallida por falta de tarjetas"""
        result = self.agent.sell(200.0, iteration=0)
        
        self.assertFalse(result)
        self.assertEqual(self.agent.cards, 0)
    
    def test_get_total_value_no_cards(self):
        """Test de valor total sin tarjetas"""
        total_value = self.agent.get_total_value(current_price=200.0)
        self.assertEqual(total_value, self.agent.balance)
    
    def test_get_total_value_with_cards(self):
        """Test de valor total con tarjetas"""
        self.agent.cards = 3
        self.agent.balance = 500.0
        current_price = 200.0
        expected_value = 500.0 + (3 * 200.0)
        
        total_value = self.agent.get_total_value(current_price)
        self.assertEqual(total_value, expected_value)


class TestMarket(unittest.TestCase):
    """Tests para la clase Market"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.market = Market()
    
    def test_initial_price(self):
        """Test que el precio inicial es correcto"""
        self.assertEqual(self.market.price, Config.INITIAL_PRICE)
    
    def test_initial_stock(self):
        """Test que el stock inicial es correcto"""
        self.assertEqual(self.market.stock, Config.INITIAL_STOCK)
    
    def test_buy_increases_price(self):
        """Test que una compra aumenta el precio en 0.5%"""
        initial_price = self.market.price
        self.market.apply_buy()
        expected_price = initial_price * (1 + Config.PRICE_INCREASE_RATE)
        self.assertAlmostEqual(self.market.price, expected_price, places=6)
    
    def test_buy_decreases_stock(self):
        """Test que una compra reduce el stock"""
        initial_stock = self.market.stock
        self.market.apply_buy()
        self.assertEqual(self.market.stock, initial_stock - 1)
    
    def test_sell_decreases_price(self):
        """Test que una venta reduce el precio en 0.5%"""
        initial_price = self.market.price
        self.market.apply_sell()
        expected_price = initial_price * (1 - Config.PRICE_DECREASE_RATE)
        self.assertAlmostEqual(self.market.price, expected_price, places=6)
    
    def test_sell_increases_stock(self):
        """Test que una venta aumenta el stock"""
        initial_stock = self.market.stock
        self.market.apply_sell()
        self.assertEqual(self.market.stock, initial_stock + 1)
    
    def test_cannot_buy_with_zero_stock(self):
        """Test que no se puede comprar sin stock"""
        self.market.stock = 0
        result = self.market.apply_buy()
        self.assertFalse(result)
    
    def test_market_state(self):
        """Test que get_state retorna el estado correcto"""
        state = self.market.get_state(iteration=10, total_iterations=1000)
        
        self.assertIsInstance(state, MarketState)
        self.assertEqual(state.price, self.market.price)
        self.assertEqual(state.stock, self.market.stock)
        self.assertEqual(state.iteration, 10)
        self.assertEqual(state.total_iterations, 1000)
    
    def test_price_history_tracking(self):
        """Test que se rastrea correctamente el historial de precios"""
        initial_length = len(self.market.price_history)
        self.market.end_iteration()
        self.assertEqual(len(self.market.price_history), initial_length + 1)
    
    def test_get_statistics(self):
        """Test que get_statistics retorna el formato correcto"""
        stats = self.market.get_statistics()
        
        self.assertIn('final_price', stats)
        self.assertIn('initial_price', stats)
        self.assertIn('price_change_pct', stats)
        self.assertIn('final_stock', stats)


class TestMarketState(unittest.TestCase):
    """Tests para MarketState"""
    
    def test_price_change_percentage_increase(self):
        """Test cálculo de cambio porcentual positivo"""
        state = MarketState(
            price=202.0,
            previous_price=200.0,
            stock=100000,
            iteration=1,
            total_iterations=1000
        )
        change = state.price_change_percentage()
        self.assertAlmostEqual(change, 0.01, places=6)  # 1% de aumento
    
    def test_price_change_percentage_decrease(self):
        """Test cálculo de cambio porcentual negativo"""
        state = MarketState(
            price=198.0,
            previous_price=200.0,
            stock=100000,
            iteration=1,
            total_iterations=1000
        )
        change = state.price_change_percentage()
        self.assertAlmostEqual(change, -0.01, places=6)  # 1% de disminución


class TestAgentDecisions(unittest.TestCase):
    """Tests para las decisiones de los agentes"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.market_state = MarketState(
            price=200.0,
            previous_price=200.0,
            stock=100000,
            iteration=0,
            total_iterations=1000
        )
    
    def test_random_agent_returns_valid_decision(self):
        """Test que RandomAgent retorna una decisión válida"""
        agent = RandomAgent(agent_id=1)
        decision = agent.decide(self.market_state, turn=0)
        self.assertIn(decision, ['buy', 'sell', 'hold'])
    
    def test_trend_agent_buys_on_price_increase(self):
        """Test que TrendAgent compra cuando el precio sube"""
        agent = TrendAgent(agent_id=1)
        state = MarketState(
            price=204.0,  # +2% respecto a 200
            previous_price=200.0,
            stock=100000,
            iteration=1,
            total_iterations=1000
        )
        
        # Ejecutar múltiples veces para verificar tendencia (75% compra)
        decisions = [agent.decide(state, turn=0) for _ in range(100)]
        buy_count = decisions.count('buy')
        
        # Debería comprar aproximadamente el 75% de las veces
        self.assertGreater(buy_count, 60)  # Al menos 60% (con margen)
    
    def test_anti_trend_agent_buys_on_price_decrease(self):
        """Test que AntiTrendAgent compra cuando el precio baja"""
        agent = AntiTrendAgent(agent_id=1)
        state = MarketState(
            price=196.0,  # -2% respecto a 200
            previous_price=200.0,
            stock=100000,
            iteration=1,
            total_iterations=1000
        )
        
        # Ejecutar múltiples veces para verificar tendencia (75% compra)
        decisions = [agent.decide(state, turn=0) for _ in range(100)]
        buy_count = decisions.count('buy')
        
        # Debería comprar aproximadamente el 75% de las veces
        self.assertGreater(buy_count, 60)  # Al menos 60% (con margen)
    
    def test_smart_agent_returns_valid_decision(self):
        """Test que SmartAgent retorna una decisión válida"""
        agent = SmartAgent(agent_id=1)
        decision = agent.decide(self.market_state, turn=0)
        self.assertIn(decision, ['buy', 'sell', 'hold'])


class TestSimulation(unittest.TestCase):
    """Tests para la clase Simulation"""
    
    def test_simulation_creates_correct_number_of_agents(self):
        """Test que se crean 100 agentes"""
        sim = Simulation()
        self.assertEqual(len(sim.agents), 100)
    
    def test_simulation_has_one_smart_agent(self):
        """Test que hay exactamente un SmartAgent"""
        sim = Simulation()
        smart_agents = [a for a in sim.agents if isinstance(a, SmartAgent)]
        self.assertEqual(len(smart_agents), 1)
    
    def test_simulation_validates_agent_count(self):
        """Test que la simulación valida el número total de agentes"""
        with self.assertRaises(ValueError):
            Simulation(num_random=50, num_trend=24, num_anti_trend=24, num_smart=1)
    
    def test_simulation_validates_iterations(self):
        """Test que la simulación valida iteraciones positivas"""
        with self.assertRaises(ValueError):
            Simulation(total_iterations=0)
    
    def test_run_iteration_returns_correct_format(self):
        """Test que run_iteration retorna el formato correcto"""
        sim = Simulation()
        buys, sells = sim.run_iteration(0)
        
        self.assertIsInstance(buys, int)
        self.assertIsInstance(sells, int)
        self.assertGreaterEqual(buys, 0)
        self.assertGreaterEqual(sells, 0)


class TestSmartAgentIntegration(unittest.TestCase):
    """Tests de integración para SmartAgent"""
    
    def test_smart_agent_ends_with_zero_cards(self):
        """Test que SmartAgent termina con 0 tarjetas después de simulación completa"""
        import random
        random.seed(42)
        
        sim = Simulation(total_iterations=100)  # Simulación corta
        sim.run(verbose=False)
        
        self.assertEqual(sim.smart_agent.cards, 0)
    
    def test_smart_agent_maintains_positive_balance(self):
        """Test que SmartAgent mantiene balance positivo"""
        import random
        random.seed(42)
        
        sim = Simulation(total_iterations=100)
        sim.run(verbose=False)
        
        self.assertGreaterEqual(sim.smart_agent.balance, 0)
    
    def test_smart_agent_performs_transactions(self):
        """Test que SmartAgent realiza transacciones"""
        import random
        random.seed(42)
        
        sim = Simulation(total_iterations=100)
        sim.run(verbose=False)
        
        self.assertGreater(len(sim.smart_agent.transactions), 0)


# TESTS EJECUTIONS

def run_tests():
    """Ejecuta todos los tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestMarket))
    suite.addTests(loader.loadTestsFromTestCase(TestMarketState))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentDecisions))
    suite.addTests(loader.loadTestsFromTestCase(TestSimulation))
    suite.addTests(loader.loadTestsFromTestCase(TestSmartAgentIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
