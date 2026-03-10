import pandas as pd
from aelogging import error, info

from AeCore.AeUtils.Aeutils import normalizar_texto


def apply_porteman_steep4(builder_instance, ruta_porteman):
    """
        Compara la descripción de las anomalías con la anotacion porteman para
        asignarles automáticamente su código, la operación y si es Vegetación o Infraestructura.

        :param builder_instance: El objeto principal con los datos del paso 3.
        :param ruta_porteman: La ruta al archivo Excel que usamos como diccionario Porteman.
        :return: No devuelve nada, actualiza la tabla con los nuevos códigos y tipos.
        """
    try:
        info(f"Paso 4: Aplicando tabla Porteman desde -> {ruta_porteman}")

        if not ruta_porteman:
            error("No se ha proporcionado la ruta del fichero Porteman.")
            return

        df_porteman = pd.read_excel(ruta_porteman)
        df_porteman.columns = [str(c).strip() for c in df_porteman.columns]

        df_main = builder_instance.product.data_dt

        if df_main.empty:
            error("El DataFrame principal está vacío.")
            return

        col_desc_port = next((c for c in df_porteman.columns if 'cruzamiento' in str(c).lower()), None)
        col_cod_port = next((c for c in df_porteman.columns if 'cod' in str(c).lower()), None)

        # pillar columnas conjunto
        col_conjunto_port = next((c for c in df_porteman.columns if 'conjunto' in str(c).lower()), None)

        col_desc_main = 'Descripción'

        if not col_desc_port or not col_cod_port:
            error("No se encontraron las columnas necesarias en Porteman.")
            return

        df_porteman['_desc_norm'] = df_porteman[col_desc_port].apply(normalizar_texto)
        df_main['_desc_norm'] = df_main[col_desc_main].apply(normalizar_texto)

        cols_interes = [c for c in df_porteman.columns if c != '_desc_norm']
        porteman_dict = df_porteman.set_index('_desc_norm')[cols_interes].to_dict('index')

        filas_actualizadas = []
        palabras_vegetacion = ['veg', 'poda', 'tala', 'arbol', 'maleza', 'rama']

        for _, row in df_main.iterrows():
            row_dict = row.to_dict()
            desc_norm = row.get('_desc_norm', '')
            desc_original = str(row.get(col_desc_main, '')).lower()

            row_dict['Codigo'] = ""
            row_dict['Operacion'] = ""
            row_dict['Tipo_Anomalia'] = 'Infraestructura'
            row_dict['Conjunto'] = ""
            datos_encontrados = None

            if desc_norm in porteman_dict:
                datos_encontrados = porteman_dict[desc_norm]
            else:
                for texto_porteman, valores in porteman_dict.items():
                    if desc_norm and texto_porteman and (desc_norm in texto_porteman or texto_porteman in desc_norm):
                        datos_encontrados = valores
                        break

            if datos_encontrados:
                row_dict['Codigo'] = datos_encontrados.get(col_cod_port, "")

                # guardamos el value de conjunto
                if col_conjunto_port:
                    row_dict['Conjunto'] = datos_encontrados.get(col_conjunto_port, "")

                col_op = next((c for c in datos_encontrados.keys() if 'operaci' in str(c).lower()), None)
                if col_op:
                    row_dict['Operacion'] = datos_encontrados.get(col_op, "")

                valores_str = " ".join([str(v).lower() for v in datos_encontrados.values()])
                if any(p in desc_original for p in palabras_vegetacion) or any(
                        p in valores_str for p in palabras_vegetacion):
                    row_dict['Tipo_Anomalia'] = 'Vegetación'
            else:
                if any(p in desc_original for p in palabras_vegetacion):
                    row_dict['Tipo_Anomalia'] = 'Vegetación'

            filas_actualizadas.append(row_dict)

        builder_instance.product.data_dt = pd.DataFrame(filas_actualizadas)
        if '_desc_norm' in builder_instance.product.data_dt.columns:
            builder_instance.product.data_dt.drop(columns=['_desc_norm'], inplace=True)

        info(f"Paso 4 completado con éxito.")

    except Exception as e:
        error(f"Error en el Paso 4: {e}")
        raise