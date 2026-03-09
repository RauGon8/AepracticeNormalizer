from abc import ABC, abstractmethod
import pandas as pd

from AeCore.AeUtils.Aeutils import (
    extract_map_and_ids_steep1,
    select_worst_hypothesis_steep2,
    combine_information_steep3,
    apply_porteman_steep4,
    link_vanos_info_steep5,
    export_final_data_steep6
)


# Guarda las tablas e informacion generada durante todo el proceso
class AeAnomaliesProduct:
    def __init__(self):
        self.step1_raw_data = pd.DataFrame()
        self.step2_filtered_data = pd.DataFrame()
        self.data_dt = pd.DataFrame()
        # para renombrar fotos
        self.image_map = {}
        # pensado para mantener estilos
        self.source_paths = {}


# Molde que obliga a tener estos pasos definidos para procesar anomalias
class Builder(ABC):

    @property
    @abstractmethod
    def product(self):
        pass

    @abstractmethod
    def read_id_anomaly_and_image(self, rutas):
        pass

    @abstractmethod
    def select_worst_hypothesis(self, ruta_combinado):
        pass

    @abstractmethod
    def combine_information(self):
        pass

    @abstractmethod
    def porteman(self, ruta_porteman):
        pass

    @abstractmethod
    def proceso_5(self, ruta_vanos):
        pass

    @abstractmethod
    def proceso_6(self, carpeta_salida, orden_trabajo):
        pass


#procesa los datos paso a paso usando Pandas
class AePandasBuilder(Builder):

    def __init__(self):
        self._product = AeAnomaliesProduct()

    @property
    def product(self):
        return self._product

    def read_id_anomaly_and_image(self, rutas_hipotesis):
        extract_map_and_ids_steep1(self, rutas_hipotesis)

    def select_worst_hypothesis(self, ruta_combinado):
        select_worst_hypothesis_steep2(self, ruta_combinado)

    def combine_information(self):
        combine_information_steep3(self)

    def porteman(self, ruta_porteman):
        apply_porteman_steep4(self, ruta_porteman)

    def proceso_5(self, ruta_vanos):
        link_vanos_info_steep5(self, ruta_vanos)

    # Paso 6: Exportar los datos
    def proceso_6(self, carpeta_salida, orden_trabajo):
        export_final_data_steep6(self, carpeta_salida, orden_trabajo)