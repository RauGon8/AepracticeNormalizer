import pandas as pd
from aelogging import info, error


def select_worst_hypothesis_steep2(builder_instance, ruta_combinado):
    """
        Lee el Excel combinado y, para cada anomalía, busca qué hipótesis climática
        tiene el peor grado de gravedad y la distancia más corta.

        :param builder_instance: El objeto principal donde guardamos los datos del programa.
        :param ruta_combinado: La ruta al archivo Excel que tiene todas las hipótesis juntas.
        :return: No devuelve nada, guarda la tabla con las peores hipotesis dentro del 'builder_instance'.
    """
    try:
        info(f"Leyendo archivo de anomalías combinadas -> {ruta_combinado}")

        #leer el archivo combinado
        df_combinado = pd.read_excel(ruta_combinado)

        #identificar dinamicamente columnas de Grado (ignorando la generica)
        columnas_grado = [
            col for col in df_combinado.columns
            if 'grado' in str(col).lower() and str(col).lower().strip() != 'grado'
        ]

        #añadimos 'incumpli' a la lista para pillar "alincumplimiento"
        columnas_distancia = [
            col for col in df_combinado.columns
            if any(palabra in str(col).lower() for palabra in ['distancia', 'dist', 'incumpli'])
        ]

        col_long = next((c for c in df_combinado.columns if 'longitud' in str(c).lower()), None)
        filas_procesadas = []

        #iterar sobre todas las anomalías del excel combinado
        for index, fila in df_combinado.iterrows():
            max_grado = -1
            min_distancia = float('inf')
            peor_hipotesis = None


            for col_g in columnas_grado:
                #extraemos el nombre de la hipotesis
                hipotesis_sufijo = str(col_g).lower().replace('grado', '').strip()

                #buscamos la columna de distancia que termine EXACTAMENTE con esa hipótesis
                col_d_match = []
                for c in columnas_distancia:
                    #split() separa el texto por espacios y saltos de linea
                    palabras_columna = str(c).lower().split()
                    #comprobamos si la ultima palabra coincide exactamente
                    if palabras_columna and palabras_columna[-1] == hipotesis_sufijo:
                        col_d_match.append(c)

                if col_d_match:
                    col_d = col_d_match[0]  # Tomamos la coincidencia exacta

                    #extraer los valores y convertirlos a número
                    grado_actual = pd.to_numeric(fila[col_g], errors='coerce')
                    distancia_actual = pd.to_numeric(fila[col_d], errors='coerce')

                    #solo evaluamos si ambos datos son validos
                    if pd.notna(grado_actual) and pd.notna(distancia_actual):

                        #mayor grado, o a igualdad de grado, menor distancia.
                        if (grado_actual > max_grado) or (
                                grado_actual == max_grado and distancia_actual < min_distancia):
                            max_grado = grado_actual
                            min_distancia = distancia_actual

                            #guardamos el sufijo en mayusculas
                            peor_hipotesis = hipotesis_sufijo.upper()

            fila_dict = fila.to_dict()
            fila_dict['Hipotesis_Seleccionada'] = peor_hipotesis
            #solo guardamos los valores si encontramos alguna hipotesis valida
            fila_dict['Grado_Final'] = max_grado if max_grado != -1 else None
            fila_dict['Distancia_Final'] = min_distancia if min_distancia != float('inf') else None

            if col_long:
                fila_dict['Longitud_Vano_Final'] = pd.to_numeric(fila[col_long], errors='coerce')

            filas_procesadas.append(fila_dict)

        #convertir a dataframe y guardar en el objeto producto
        df_filtrado = pd.DataFrame(filas_procesadas)
        builder_instance.product.step2_filtered_data = df_filtrado

        info(f"Paso 2 completado. {len(df_filtrado)} anomalias filtradas por la peor hipotesis.")

    except Exception as e:
        error(f"Error critico en el Paso 2 procesando '{ruta_combinado}' -> {e}")
        raise