from PySide6.QtCore import QThread, Signal
from AeCore.AeLogic import AeFacade
from aelogging import info, error


class Worker(QThread):
    progress = Signal(int, str)
    finished = Signal(list)
    error_signal = Signal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        """
        punto entrada del hilo

        llamamos al facade para que lance la construccion de pasos
        :return:
        """
        try:
            info("Worker: iniciando proceso en segundo plano.")

            facade = AeFacade()

            result = facade.run_full_process(
                config=self.config,
                progress_callback=self._emit_progress
            )

            info("Worker: proceso completado correctamente.")
            self.finished.emit(result)

        except Exception as e:
            msg = f"Worker: error durante la ejecución → {str(e)}"
            error(msg)
            self.error_signal.emit(msg)

    def _emit_progress(self, percent, message):
        """
        este metodo lo usa el director para actualizar el estado de los distintos pasos

        """
        self.progress.emit(percent, message)
