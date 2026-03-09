from AeCore.AeLogic.AeBuilder.director import AeDirector
from AeCore.AeLogic.AeBuilder.builder import AePandasBuilder
from aelogging import info, error

# Puerta de entrada unica para que la interfaz inicie el proceso facilmente
class AeFacade:
    def __init__(self):
        pass

    # Prepara los trabajadores, inicia los pasos y controla si hay fallos
    def run_full_process(self, config, progress_callback=None):
        info("Iniciando la secuencia de construcción")

        builder = self._create_builder()

        director = AeDirector(
            builder=builder,
            config=config,
            progress_callback=progress_callback
        )

        try:
            anomalies_product = director.run()
            info("Construcción completada exitosamente.")
            return anomalies_product

        except Exception as e:
            error(f"Error crítico en Facade → {e}")
            raise

    # Crea el trabajador encargado de manipular los datos reales
    def _create_builder(self):
        info("Instanciando AePandasBuilder...")
        return AePandasBuilder()