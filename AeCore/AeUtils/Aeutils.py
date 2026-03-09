
import pandas as pd



column_alias = {
    "ID_ANOMALIA": ["Nº de anomalía", "ID", "Anomalia_ID", "Número"],
    "GRADO": ["Grado", "Nivel", "Severidad", "Grado de anomalía"],
    "DISTANCIA": ["Distancia", "Metros", "Dist", "Mínima distancia absoluta de (h) a la trayectoria del cable"],
    "VANO": ["Vano", "Tramo", "Span"],
    "DENOMINACION_UT": ["Denominación UT", "Denominacion UT", "Denominacion", "Denominación"],
    "UBICACION_TECNICA": ["Ubicación Tecnica", "Ubicacion Tecnica", "Ubicación Técnica", "UT"],
    "x": ["X", "Coordenada X", "UTM (X)"],
    "y": ["Y", "Coordenada Y", "UTM (Y)"],
    "z": ["Z", "Coordenada Z", "UTM (Z)"],
    "huso": ["Huso", "Zona"],
    "CIRCUITO": ["Circuito", "Nombre de Circuito", "Nemónico circuito", "Línea"],
    "LONGITUD_VANO": ["Longitud vano", "Longitud", "Distancia Vano"],
    "DMR": ["DMR"],
    "APOYO_INI": ["Nº apoyo (a) inicial", "Apoyo Inicial"],
    "APOYO_FIN": ["Nº apoyo (b) final", "Nº apoyo (a) final", "Apoyo Final"],
    "TENSION": ["Tensión (kV)", "Tensión"],
    "TIPO_ANO": ["Tipo de anomalía"],
    "REGLAMENTO": ["Se aplica el reglamento", "Reglamento"],
    "DIST_REGLA": ["Distancia de reglamento"],
    "CUMPLE": [
        "Cumple/incumple por +/- (m)",
        "Cumple/incumple por +/-",
        "+/- distancia vertical (w) del cable a la cota de (h)",
        "+/- distancia horizontal (v) del punto (h) a la vertical del cable",
        "'+/- distancia vertical (w) del cable a la cota de (h)",
        "'+/- distancia horizontal (v) del punto (h) a la vertical del cable"
    ],
    "NOTAS": ["Notas y/o aclaraciones", "Notas", "Observaciones"],
    "TEMP_MAX": [
        "Temperatura máxima distinta",
        "Temperatura maxima distinta",
        "Temp ºC",
        "Temp. ºC",
        "Temperatura max de diseño de la linea",
        "Temperatura",
        "Temperatura máxima a aplicar"
    ],
    "FASE": ["Fase/CT", "Fase/CT en la que se encuentra el incumplimiento"],
    "DIST_APOYO": [
        "Distancia al apoyo más cercano",
        "Distancia al apoyo mas cercano",
        "Distancia al\napoyo  más\ncercano",
        "Distancia al apoyo  más cercano",
        "Distancia al apoyo",
        "Distancia al primer apoyo del vano"
    ]
}

def normalizar_texto(valor):
    """
        Limpia un texto quitándole espacios, tabulaciones y saltos de línea,
        y lo pasa a minúsculas para que sea fácil compararlo con otros textos.

        :param valor: El texto original que queremos limpiar.
        :return: El texto limpio en formato cadena.
        """
    if pd.isna(valor):
        return ""
    return str(valor).replace(" ","").replace("\t","").replace("\n","").strip().lower()


#reutilizo mi metodo para leer filas en los xls
def localizar_posiciones_cabeceras(hoja_lectura):
    """
    Escanea las primeras filas de un Excel como un radar para buscar
    los títulos de las columnas, usando nuestra lista de alias.

    :param hoja_lectura: La pestaña del archivo Excel que estamos escaneando.
    :return: Un diccionario con el nombre de la columna y sus coordenadas exactas (fila, columna).
    """
    posiciones={}
    #recorremos las primeras 20 filas

    for indice_fila in range (min(20,hoja_lectura.nrows)):
        #revisamos las columnas que tengan los datos de ncols
        for indice_columna in range (hoja_lectura.ncols):
            #cogemos el valor de cada celda, lo pasamos a str y luego le quitamos los espacios con el strip
            valor_celda=str(hoja_lectura.cell_value(indice_fila,indice_columna)).strip()

            #revisamos si el valor de la celda coincide con algun alias del diccionario
            for clave, lista_de_alias in column_alias.items():
                #comprobamos si encuentra una coincidencia y lo añade a posiciones, si encuentra x por ejemplo
                # no vuelve a buscarlo porque ya lo obtuvo (if clave not in posiciones)
                if clave not in posiciones:

                    #comparamos el valor con mi lista de column alias
                    if any(alias.lower()==valor_celda.lower()
                           for alias in lista_de_alias):
                        posiciones[clave]=(indice_fila,indice_columna)
    return posiciones
