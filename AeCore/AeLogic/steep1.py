#lee informes y guarda datos normalizados
import os

import pandas as pd
import xlrd
from aelogging import info

from AeCore.AeUtils.Aeutils import localizar_posiciones_cabeceras, normalizar_texto


def extract_map_and_ids_steep1(builder_instance, rutas_hipotesis: list):
    """
    :param builder_instance:
    :param rutas_hipotesis:
    :return:
    """
    info("Procesando y normalizando identificadores de forma continua...")
    all_tables = []
    contador_global = 0

    for ruta_carpeta in rutas_hipotesis:
        nombre_hoja = os.path.basename(ruta_carpeta)
        archivos = [
            archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.xls')
        ]

        if not archivos: continue

        ruta_xls = os.path.join(ruta_carpeta, archivos[0])
        builder_instance.product.source_paths[nombre_hoja] = ruta_xls

        libro = xlrd.open_workbook(ruta_xls)
        hoja = libro.sheet_by_index(0)
        coords = localizar_posiciones_cabeceras(hoja)

        if "ID_ANOMALIA" in coords:
            fila_cabecera, columna_id = coords["ID_ANOMALIA"]

            # leemos y limpiamos filas vacías
            df_temp = pd.read_excel(ruta_xls, skiprows=fila_cabecera)
            df_temp = df_temp.dropna(how='all')

            # renombrado de columnas segun alias
            mapeo = {}
            for clave, (f, c) in coords.items():
                if c < len(df_temp.columns):
                    nombre_actual_columna = df_temp.columns[c]
                    mapeo[nombre_actual_columna] = clave

            df_temp = df_temp.rename(columns=mapeo)


            #si 'GRADO' no existe, lo buscamos manualmente
            if 'GRADO' not in df_temp.columns:
                col_grado_alternativa = next((c for c in df_temp.columns if 'grado' in str(c).lower()), None)
                if col_grado_alternativa:
                    df_temp = df_temp.rename(columns={col_grado_alternativa: 'GRADO'})


            # procesamos siempre
            if 'ID_ANOMALIA' in df_temp.columns:
                df_temp = df_temp.dropna(subset=['ID_ANOMALIA'])

                #volvemos añadir vano normal
                if 'VANO' in df_temp.columns:
                    df_temp['VANO_NORM'] = df_temp['VANO'].apply(normalizar_texto)

                if 'CIRCUITO' in df_temp.columns:
                    df_temp['CIRC_NORM'] = df_temp['CIRCUITO'].apply(normalizar_texto)

                nuevos_ids = []

                for _, fila in df_temp.iterrows():
                    id_original_excel = str(fila.iloc[columna_id]).split('.')[0]
                    id_nuevo = contador_global
                    nuevos_ids.append(id_nuevo)

                    builder_instance.product.image_map[id_nuevo] = {
                        "archivo_foto_original": id_original_excel,
                        "carpeta_origen": ruta_carpeta,
                        "hipotesis": nombre_hoja
                    }
                    contador_global += 1

                df_temp['Nº de anomalia'] = nuevos_ids
                df_temp['hipotesis_origen'] = nombre_hoja
                all_tables.append(df_temp)

    if all_tables:
        builder_instance.product.step1_raw_data = pd.concat(all_tables, ignore_index=True)
        builder_instance.product.data_dt = builder_instance.product.step1_raw_data

        print(f"Paso 1 terminado. {contador_global} anomalias procesadas.")