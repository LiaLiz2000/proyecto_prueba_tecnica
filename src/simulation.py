"""
Orquestación de la simulación
"""

import random
from typing import List, Tuple

from .config import Config
from .market import Market
from .agents import Agent, RandomAgent, TrendAgent, AntiTrendAgent, SmartAgent


class Simulation:
    """
    Clase principal que orquesta la simulación del mercado
    
    Gestiona la creación de agentes, la ejecución de iteraciones y
    la presentación de resultados
    """
    
    def __init__(
        self,
        num_random: int = Config.NUM_RANDOM,
        num_trend: int = Config.NUM_TREND,
        num_anti_trend: int = Config.NUM_ANTI_TREND,
        num_smart: int = Config.NUM_SMART,
        total_iterations: int = Config.TOTAL_ITERATIONS
    ):
        """
        Inicializa la simulación.
        
        Args:
            num_random: Número de RandomAgents
            num_trend: Número de TrendAgents
            num_anti_trend: Número de AntiTrendAgents
            num_smart: Número de SmartAgents
            total_iterations: Total de iteraciones a ejecutar
        
        Raises:
            ValueError: Si la configuración es inválida
        """
        # Validar configuración
        total_agents = num_random + num_trend + num_anti_trend + num_smart
        if total_agents != 100:
            raise ValueError(f"El total de agentes debe ser 100, actual: {total_agents}")
        
        if total_iterations <= 0:
            raise ValueError("El número de iteraciones debe ser positivo")
        
        self.total_iterations = total_iterations
        self.market = Market()
        self.agents: List[Agent] = []
        
        # Crear agentes
        agent_id = 0
        
        for _ in range(num_random):
            self.agents.append(RandomAgent(agent_id))
            agent_id += 1
        
        for _ in range(num_trend):
            self.agents.append(TrendAgent(agent_id))
            agent_id += 1
        
        for _ in range(num_anti_trend):
            self.agents.append(AntiTrendAgent(agent_id))
            agent_id += 1
        
        for _ in range(num_smart):
            self.agents.append(SmartAgent(agent_id))
            agent_id += 1
        
        # Referencia directa al agente inteligente
        self.smart_agent = self.agents[-1]
    
    def run_iteration(self, iteration: int) -> Tuple[int, int]:
        """
        Ejecuta una iteración completa del mercado.
        
        Args:
            iteration: Número de iteración actual
        
        Returns:
            Tuple[int, int]: (número de compras, número de ventas)
        """
        # Ordenar agentes aleatoriamente para fairness
        shuffled_agents = self.agents.copy()
        random.shuffle(shuffled_agents)
        
        buys = 0
        sells = 0
        
        for turn, agent in enumerate(shuffled_agents):
            market_state = self.market.get_state(iteration, self.total_iterations)
            decision = agent.decide(market_state, turn)
            
            if decision == 'buy' and agent.can_buy(self.market.price):
                if self.market.stock > 0:
                    agent.buy(self.market.price, iteration)
                    self.market.apply_buy()
                    buys += 1
            
            elif decision == 'sell' and agent.can_sell():
                agent.sell(self.market.price, iteration)
                self.market.apply_sell()
                sells += 1
        
        self.market.volume_history.append(buys + sells)
        self.market.end_iteration()
        
        return buys, sells
    
    def run(self, verbose: bool = True):
        """
        Ejecuta la simulación completa.
        
        Args:
            verbose: Si True, imprime información durante la ejecución
        """
        if verbose:
            self._print_header()
        
        for iteration in range(self.total_iterations):
            buys, sells = self.run_iteration(iteration)
            
            if verbose and (iteration + 1) % 100 == 0:
                print(f"Iteración {iteration + 1:4d}: "
                      f"Precio=${self.market.price:8.2f} | "
                      f"Stock={self.market.stock:6,} | "
                      f"Compras={buys:2d} | Ventas={sells:2d}")
        
        if verbose:
            self._print_results()
    
    def _print_header(self):
        """Imprime el encabezado de la simulación"""
        print("=" * 60)
        print("SIMULACIÓN DEL MERCADO DE TARJETAS GRÁFICAS")
        print("=" * 60)
        print(f"Precio inicial: ${self.market.price:.2f}")
        print(f"Stock inicial: {self.market.stock:,} unidades")
        print(f"Total de agentes: {len(self.agents)}")
        print(f"  - RandomAgent: {Config.NUM_RANDOM}")
        print(f"  - TrendAgent: {Config.NUM_TREND}")
        print(f"  - AntiTrendAgent: {Config.NUM_ANTI_TREND}")
        print(f"  - SmartAgent: {Config.NUM_SMART}")
        print(f"Iteraciones: {self.total_iterations:,}")
        print("=" * 60)
    
    def _print_results(self):
        """Imprime los resultados finales de la simulación"""
        print("\n" + "=" * 60)
        print("RESULTADOS FINALES")
        print("=" * 60)
        
        final_price = self.market.price
        
        # Clasificar agentes por tipo
        agent_types = {
            'RandomAgent': [],
            'TrendAgent': [],
            'AntiTrendAgent': [],
            'SmartAgent': []
        }
        
        for agent in self.agents:
            agent_types[agent.__class__.__name__].append(agent)
        
        market_stats = self.market.get_statistics()
        print(f"\nPrecio final: ${market_stats['final_price']:.2f}")
        print(f"Cambio de precio: {market_stats['price_change_pct']:+.2f}%")
        print(f"Stock final: {market_stats['final_stock']:,} unidades")
        print(f"Precio máximo alcanzado: ${market_stats['max_price']:.2f}")
        print(f"Precio mínimo alcanzado: ${market_stats['min_price']:.2f}")
        
        print("\n" + "-" * 60)
        print("RESUMEN POR TIPO DE AGENTE")
        print("-" * 60)
        
        for agent_type, agents in agent_types.items():
            if not agents:
                continue
            
            total_values = [a.get_total_value(final_price) for a in agents]
            
            print(f"\n{agent_type} ({len(agents)} agentes):")
            print(f"  Balance promedio: ${sum(a.balance for a in agents)/len(agents):.2f}")
            print(f"  Tarjetas promedio: {sum(a.cards for a in agents)/len(agents):.1f}")
            print(f"  Valor total promedio: ${sum(total_values)/len(total_values):.2f}")
            print(f"  Mejor agente: ${max(total_values):.2f}")
            print(f"  Peor agente: ${min(total_values):.2f}")
        
        # Detalle del SmartAgent
        print("\n" + "-" * 60)
        print("DETALLE DEL SMARTAGENT")
        print("-" * 60)
        smart = self.smart_agent
        print(f"Balance final: ${smart.balance:.2f}")
        print(f"Tarjetas restantes: {smart.cards}")
        print(f"Valor total: ${smart.get_total_value(final_price):.2f}")
        print(f"Ganancia/Pérdida: ${smart.balance - Config.INITIAL_BALANCE:+.2f}")
        print(f"Retorno: {((smart.get_total_value(final_price) / Config.INITIAL_BALANCE) - 1) * 100:+.2f}%")
        print(f"Transacciones realizadas: {len(smart.transactions)}")
        
        if smart.cards > 0:
            print(f"\n El agente no terminó todas sus tarjetas")
            print(f"   Tarjetas restantes: {smart.cards}")
        else:
            print(f"\n✓ El agente terminó con 0 tarjetas (requisito cumplido)")
        
        # Ranking top 10
        print("\n" + "-" * 60)
        print("TOP 10 AGENTES POR VALOR TOTAL")
        print("-" * 60)
        sorted_agents = sorted(
            self.agents,
            key=lambda a: a.get_total_value(final_price),
            reverse=True
        )
        
        for i, agent in enumerate(sorted_agents[:10], 1):
            total_value = agent.get_total_value(final_price)
            marker = "🏆" if isinstance(agent, SmartAgent) else "  "
            print(f"{marker} {i:2d}. {agent.__class__.__name__:<18} (ID:{agent.agent_id:2d}): "
                  f"${total_value:8.2f} "
                  f"(${agent.balance:7.2f} + {agent.cards:2d} tarjetas)")
        
        print("=" * 60)
