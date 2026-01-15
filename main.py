"""
Punto de entrada para la simulación del mercado
"""
#imports

from src import Config, Simulation

def main():
    """
    Función principal de ejecución.
    """
    # Validar configuración
    Config.validate()
    
    # Crear y ejecutar simulación
    simulation = Simulation()
    simulation.run(verbose=True)


if __name__ == "__main__":
    main()
