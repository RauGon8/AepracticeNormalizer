from PySide6.QtCore import QThread, Signal
from aelogging import info, error

from AeCore.AeLogic.AeFacade.facade import AeFacade

class Worker(QThread):
    progress = Signal(int, str)
    finished = Signal(object)
    error_signal = Signal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        """
        punto entrada del hilo
        llamamos al facade para que lance la construccion de pasos
        """
        try:
            info("Worker: iniciando proceso en segundo plano.")

            facade = AeFacade()

            # Lanzamos todo el proceso pesado
            result = facade.run_full_process(
                config=self.config,
                progress_callback=self._emit_progress
            )

            info("Worker: proceso completado correctamente.")
            # Enviamos el resultado a la ventana principal
            self.finished.emit(result)

        except Exception as e:
            msg = f"Worker: error durante la ejecución → {str(e)}"
            error(msg)
            # Avisamos a la ventana de que algo exploto
            self.error_signal.emit(msg)

    def _emit_progress(self, percent, message):
        """
        este metodo lo usa el director para actualizar el estado de los distintos pasos
        """
        self.progress.emit(percent, message)