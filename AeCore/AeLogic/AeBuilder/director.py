from aelogging import info, error


# Controla el orden exacto en el que se hacen los pasos
class AeDirector:
    def __init__(self, builder, config, progress_callback=None):
        self.builder = builder
        self.config = config
        self.progress_callback = progress_callback

    # Manda el progreso a la barra de carga de la interfaz
    def _progress(self, value, message=""):
        if self.progress_callback:
            self.progress_callback(value, message)
        info(f"Director: {message}")

    # Limpia y prepara las variables que vienen de la configuracion
    def _extraer_rutas(self):
        rutas_maestras = self.config.get('rutas_maestras', {})

        ruta_combinado = rutas_maestras.get(0, rutas_maestras.get('0', ['']))
        ruta_combinado = ruta_combinado[0] if ruta_combinado else ''

        rutas_hipotesis = rutas_maestras.get(1, rutas_maestras.get('1', []))

        ruta_porteman = rutas_maestras.get(2, rutas_maestras.get('2', ['']))
        ruta_porteman = ruta_porteman[0] if ruta_porteman else ''

        ruta_vanos = rutas_maestras.get(3, rutas_maestras.get('3', ['']))
        ruta_vanos = ruta_vanos[0] if ruta_vanos else ''

        carpeta_salida = self.config.get('carpeta_salida', '')
        orden_trabajo = self.config.get('orden_trabajo', '')

        return ruta_combinado, rutas_hipotesis, ruta_porteman, ruta_vanos, carpeta_salida, orden_trabajo

    # Ejecuta todos los pasos en orden y devuelve el resultado final
    def run(self):
        try:
            ruta_combinado, rutas_hipotesis, ruta_porteman, ruta_vanos, carpeta_salida, orden_trabajo = self._extraer_rutas()

            self._progress(10, "Paso 1: Extrayendo mapas e IDs...")
            self.builder.read_id_anomaly_and_image(rutas_hipotesis)

            self._progress(30, "Paso 2: Seleccionando la peor hipótesis...")
            self.builder.select_worst_hypothesis(ruta_combinado)

            self._progress(50, "Paso 3: Ejecutando unión de información...")
            self.builder.combine_information()

            self._progress(65, "Paso 4: Aplicando agrupación Porteman...")
            self.builder.porteman(ruta_porteman)

            self._progress(80, "Paso 5: Vinculando información de vanos...")
            self.builder.proceso_5(ruta_vanos)

            self._progress(90, "Paso 6: Exportando Excel e imágenes...")
            self.builder.proceso_6(carpeta_salida, orden_trabajo)

            self._progress(100, "Proceso completado con éxito.")
            return self.builder.product

        except Exception as e:
            error(f"Error crítico durante la ejecución del Director → {e}")
            raise