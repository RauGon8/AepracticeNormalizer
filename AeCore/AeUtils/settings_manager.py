import json
import os


class SettingsManager:
    def __init__(self, filepath="ae_session.json"):
        self.filepath = filepath

    #devuelve los valores base con el neon desactivado por defecto
    def obtener_defaults(self):
        return {
            "neon_activo": False,
            "neon_color": "#00beff",
            "tema": "defecto",
            "rutas_guardadas": {"0": [], "1": [], "2": [], "3": []},
            "tipo_archivo_seleccionado": 0,
            "orden_trabajo_texto": ""
        }

    # lee el archivo de forma segura y aplica valores por defecto si el json falla
    def cargar_ajustes(self):
        defaults = self.obtener_defaults()
        if not os.path.exists(self.filepath):
            return defaults

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                #si el archivo existe pero esta vacio evitamos que crashee
                if not contenido:
                    return defaults

                datos = json.loads(contenido)

                # rellenamos las claves que falten con los defaults
                for key, value in defaults.items():
                    if key not in datos:
                        datos[key] = value
                return datos
        except Exception as e:
            print(f"error al leer json, usando defaults: {e}")
            return defaults

    #guarda las rutas al cerrar la ventana principal
    def guardar_ajustes(self, rutas, combo_index, orden_texto):
        datos = self.cargar_ajustes()

        datos["rutas_guardadas"] = rutas
        datos["tipo_archivo_seleccionado"] = combo_index
        datos["orden_trabajo_texto"] = orden_texto

        self.guardar_ajustes_completos(datos)

    # guarda el diccionario entero desde la ventana de configuracion
    def guardar_ajustes_completos(self, diccionario_ajustes):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(diccionario_ajustes, f, indent=4)
        except Exception as e:
            print(f"error critico guardando json: {e}")