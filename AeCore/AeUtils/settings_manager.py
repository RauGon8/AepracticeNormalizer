import json
from PySide6.QtCore import QSettings


class SettingsManager:

    def __init__(self):
        # qsettings gestiona el archivo nativo automaticamente
        self.settings = QSettings("AeTools", "AePracticeNormalizer")

    def obtener_defaults(self):
        """
        Genera un diccionario con los valores iniciales para cuando el programa se abre
        por primera vez o le faltan datos.

        :return: Diccionario con la configuración por defecto.
        """
        # devuelve los valores base con el neon activado por defecto
        return {
            "neon_activo": True,
            "neon_color": "#00beff",
            "tema": "defecto",
            "rutas_guardadas": {"0": [], "1": [], "2": [], "3": []},
            "tipo_archivo_seleccionado": 0,
            "orden_trabajo_texto": ""
        }

    def cargar_ajustes(self):
        """
        Lee los datos almacenados en QSettings de forma segura y rellena con
        los defaults si falta algo.

        :return: Diccionario con los datos listos para usarse en la interfaz.
        """
        defaults = self.obtener_defaults()
        datos = {}

        # rescatamos los valores nativos forzando el tipo correcto
        datos["neon_activo"] = self.settings.value("neon_activo", defaults["neon_activo"], type=bool)
        datos["neon_color"] = self.settings.value("neon_color", defaults["neon_color"], type=str)
        datos["tema"] = self.settings.value("tema", defaults["tema"], type=str)

        # las rutas complejas las leemos como string json para no perder el formato
        rutas_str = self.settings.value("rutas_guardadas", None, type=str)
        if rutas_str:
            try:
                datos["rutas_guardadas"] = json.loads(rutas_str)
            except Exception as e:
                print(f"error al parsear rutas de qsettings: {e}")
                datos["rutas_guardadas"] = defaults["rutas_guardadas"]
        else:
            datos["rutas_guardadas"] = defaults["rutas_guardadas"]

        # leemos el resto de valores simples de la interfaz principal
        datos["tipo_archivo_seleccionado"] = self.settings.value("tipo_archivo_seleccionado",defaults["tipo_archivo_seleccionado"], type=int)
        datos["orden_trabajo_texto"] = self.settings.value("orden_trabajo_texto", defaults["orden_trabajo_texto"],type=str)

        return datos

    def guardar_ajustes(self, rutas, combo_index, orden_texto):
        """
        Guarda los datos rápidos de la interfaz principal al cerrar la ventana.

        :param rutas: Diccionario con las listas de archivos subidos por el usuario.
        :param combo_index: Número de la pestaña seleccionada en el combo box.
        :param orden_texto: Texto con la orden de trabajo introducido por el usuario.
        :return: No devuelve nada.
        """
        # cargamos primero para no machacar lo que hubiera de la ventana de ajustes
        datos = self.cargar_ajustes()

        datos["rutas_guardadas"] = rutas
        datos["tipo_archivo_seleccionado"] = combo_index
        datos["orden_trabajo_texto"] = orden_texto

        self.guardar_ajustes_completos(datos)

    def guardar_ajustes_completos(self, diccionario_ajustes):
        """
        Guarda el diccionario entero de preferencias.

        :param diccionario_ajustes: El diccionario completo con todos los ajustes listos para guardar.
        :return: No devuelve nada.
        """
        self.settings.setValue("neon_activo", diccionario_ajustes.get("neon_activo"))
        self.settings.setValue("neon_color", diccionario_ajustes.get("neon_color"))
        self.settings.setValue("tema", diccionario_ajustes.get("tema"))

        # convertimos las rutas a json string para proteger la estructura original
        self.settings.setValue("rutas_guardadas", json.dumps(diccionario_ajustes.get("rutas_guardadas", {})))

        self.settings.setValue("tipo_archivo_seleccionado", diccionario_ajustes.get("tipo_archivo_seleccionado"))
        self.settings.setValue("orden_trabajo_texto", diccionario_ajustes.get("orden_trabajo_texto"))

        # forzamos la escritura en disco para evitar perdidas si el programa se cierra de golpe
        self.settings.sync()