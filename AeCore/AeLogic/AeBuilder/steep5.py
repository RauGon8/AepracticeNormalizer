import pandas as pd
from aelogging import info, error


def link_vanos_info_steep5(builder_instance, ruta_vanos):
    """
        Busca el vano de cada anomalía en el archivo de vanos para
        averiguar su "Ubicación Técnica" (UT) exacta,
        separando si es un vano de infraestructura o de vegetación.

        :param builder_instance: El objeto principal con los datos del paso 4.
        :param ruta_vanos: La ruta al archivo excel que contiene la lista oficial de vanos y UTs.
        :return: No devuelve nada, añade la columna de ubicacion tecnica terminada a la tabla.
    """
    info("Paso 5: Vinculando información de vanos")
    try:
        df_p = builder_instance.product.data_dt
        df_vanos = pd.read_excel(ruta_vanos)

        #buscamos las columnas de forma dinamica
        col_vano_anomalias = next(
            (c for c in df_p.columns if 'vano' in str(c).lower() and 'long' not in str(c).lower()), None)

        if not col_vano_anomalias:
            df_p['Ubicación Técnica'] = ""
            builder_instance.product.data_dt = df_p
            return

        df_vanos.columns = [str(c).lower().strip() for c in df_vanos.columns]
        col_denominacion = next((col for col in df_vanos.columns if 'denominaci' in col), None)
        col_ubicacion = next((col for col in df_vanos.columns if 'ubicaci' in col), None)

        if not col_denominacion or not col_ubicacion:
            #a nivel de columna entera si no hay maestro
            df_p['Ubicación Técnica'] = df_p[col_vano_anomalias]
            builder_instance.product.data_dt = df_p
            return

        def obtener_ut(fila):
            vano_anomalia = str(fila.get(col_vano_anomalias, '')).replace(" ", "").strip()
            # aseguramos que pillamos bien el tipo de anomalía
            tipo_anomalia = str(fila.get('Tipo_Anomalia', '')).lower().strip()
            es_vegetacion = 'vegetaci' in tipo_anomalia

            if not vano_anomalia or vano_anomalia == 'nan':
                return ""

            # i  nvertimos el vano (de 571-572 a 572-571) por si en el maestro esta al reves
            partes = vano_anomalia.split('-')
            if len(partes) == 2:
                vano_inverso = f"{partes[1]}-{partes[0]}"
            else:
                vano_inverso = vano_anomalia

            serie_denominacion = df_vanos[col_denominacion].astype(str)
            serie_ubicacion = df_vanos[col_ubicacion].astype(str)

            # buscamos coincidencias con guiones para ser exactos
            vano_busqueda_1 = f"-{vano_anomalia}-"
            vano_busqueda_2 = f"-{vano_inverso}-"

            mask = serie_denominacion.str.contains(vano_busqueda_1, regex=False, na=False) | \
                   serie_denominacion.str.contains(vano_busqueda_2, regex=False, na=False)

            coincidencias = df_vanos[mask]

            # si no hay con guiones, probamos el vano en bruto
            if coincidencias.empty:
                mask_fallback = serie_denominacion.str.contains(vano_anomalia, regex=False, na=False) | \
                                serie_denominacion.str.contains(vano_inverso, regex=False, na=False)
                coincidencias = df_vanos[mask_fallback]

            # si no se encuentra en el maestro, devolvemos el vano original
            if coincidencias.empty:
                return vano_anomalia

            # reglas para v y vf
            valores_ut = coincidencias[col_ubicacion].astype(str).str.strip()

            #si es de vegetacion empezara por VF, sino empezara por v
            if es_vegetacion:

                match = valores_ut[valores_ut.str.startswith('VF', na=False)]
                if not match.empty:
                    return match.iloc[0]
                else:
                    # encontrado pero sin VF, devolvemos vano
                    return vano_anomalia
            else:

                match = valores_ut[
                    valores_ut.str.startswith('V', na=False) & ~valores_ut.str.startswith('VF', na=False)]
                if not match.empty:
                    return match.iloc[0]
                else:
                    # encontrado pero sin V, devolvemos vano
                    return vano_anomalia

        #guardamos
        df_p['Ubicación Técnica'] = df_p.apply(obtener_ut, axis=1)
        builder_instance.product.data_dt = df_p
        info("Paso 5 completado con éxito.")

    except Exception as e:
        error(f"Error en el Paso 5: {e}")
        # En caso de error fatal, rellenar con el vano
        col_vano = next((c for c in builder_instance.product.data_dt.columns if
                         'vano' in str(c).lower() and 'long' not in str(c).lower()), None)
        if col_vano:
            builder_instance.product.data_dt['Ubicación Técnica'] = builder_instance.product.data_dt[col_vano]
