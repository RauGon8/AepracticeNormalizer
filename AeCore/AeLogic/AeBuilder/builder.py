from abc import ABC, abstractmethod
import pandas as pd

from AeCore.AeLogic.steep1 import extract_map_and_ids_steep1
from AeCore.AeLogic.steep2 import select_worst_hypothesis_steep2
from AeCore.AeLogic.steep3 import combine_information_steep3
from AeCore.AeLogic.steep4 import apply_porteman_steep4
from AeCore.AeLogic.steep5 import link_vanos_info_steep5
from AeCore.AeLogic.steep6 import export_final_data_steep6


class AeAnomaliesProduct:
    def __init__(self)-> None:
        self.step1_raw_data = pd.DataFrame()

        self.step2_filtered_data = pd.DataFrame()

        self.data_dt= pd.DataFrame()
        #para renombrar fotos
        self.image_map={}
        #pensado para mantener estilos
        self.source_paths={}


class Builder(ABC):

    @property
    #usamos property para que el director pueda acceder al resultado de los metodos como un atributo
    @abstractmethod
    def product(self) :
        pass

    @abstractmethod
    def read_id_anomaly_and_image(self,rutas):
        pass

    @abstractmethod
    def select_worst_hypothesis(self, ruta_combinado):
        pass

    @abstractmethod
    def combine_information(self) :
        pass

    @abstractmethod
    def porteman(self, ruta_porteman) :
        pass

    @abstractmethod
    def proceso_5(self, ruta_vanos):
        pass

    @abstractmethod
    def proceso_6(self,carpeta_salida, orden_trabajo):
        pass


#procesa los datos paso a paso usando Pandas
class AePandasBuilder(Builder):

    def __init__(self):
        self._product = AeAnomaliesProduct()

    @property
    def product(self) -> AeAnomaliesProduct:


        return self._product

    def read_id_anomaly_and_image(self,rutas_hipotesis):
        extract_map_and_ids_steep1(self,rutas_hipotesis)

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