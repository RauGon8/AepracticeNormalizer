import pandas as pd
from aelogging import info

from AeCore.AeUtils.Aeutils import normalizar_texto


#cruzamos informacion de los combinados con los informes
def combine_information_steep3(builder_instance):
    """
    Cruza los datos de las peores hipótesis con la información cruda del principio
    para recuperar datos técnicos vitales como las coordenadas, el vano y el circuito.

    :param builder_instance: El objeto principal que ya contiene las tablas de los pasos 1 y 2.
    :return: No devuelve nada, guarda la tabla combinada y enriquecida en el 'builder_instance'.
    """
    info("Paso 3: Uniendo anomalias (Comparando...)")

    df_comb = builder_instance.product.step2_filtered_data
    df_inf = builder_instance.product.step1_raw_data

    # Prevenir el error de fillna
    if 'GRADO' in df_inf.columns:
        df_inf['GRADO_NUM'] = pd.to_numeric(df_inf['GRADO'], errors='coerce').fillna(0).astype(int)
    else:
        df_inf['GRADO_NUM'] = 0

    col_vano_c = next((c for c in df_comb.columns if 'vano' in str(c).lower() and 'long' not in str(c).lower()), None)
    col_cir_c = next((c for c in df_comb.columns if 'circuito' in str(c).lower()), None)
    col_dist_inf = 'DISTANCIA' if 'DISTANCIA' in df_inf.columns else next(
        (c for c in df_inf.columns if 'dist' in str(c).lower()), None)

    if col_dist_inf:
        df_inf = df_inf.copy()
        df_inf['DIST_CALC'] = pd.to_numeric(df_inf[col_dist_inf].astype(str).str.replace(',', '.'), errors='coerce')

    filas_finales = []
    ids_asignados = set()
    col_desc_comb = next((c for c in df_comb.columns if 'descrip' in str(c).lower()), None)

    # Variables técnicas base
    cols_tecnicas = ['x', 'y', 'z', 'huso', 'REGLAMENTO', 'DIST_REGLA', 'APOYO_INI', 'APOYO_FIN', 'TENSION',
                     'LONGITUD_VANO', 'TIPO_ANO', 'CUMPLE', 'NOTAS', 'TEMP_MAX', 'FASE', 'DMR', 'VANO', 'CIRCUITO',
                     'DIST_APOYO']

    for idx, row_c in df_comb.iterrows():
        hipo_c = normalizar_texto(row_c.get('Hipotesis_Seleccionada'))
        vano_c = normalizar_texto(row_c.get(col_vano_c))
        dist_c_num = pd.to_numeric(str(row_c.get('Distancia_Final')).replace(',', '.'), errors='coerce')

        candidatos = df_inf[df_inf['hipotesis_origen'].apply(normalizar_texto) == hipo_c].copy()

        if not candidatos.empty and pd.notna(dist_c_num) and 'DIST_CALC' in candidatos.columns:
            candidatos['_diferencia'] = (candidatos['DIST_CALC'] - dist_c_num).abs()
            candidatos = candidatos.sort_values(by='_diferencia')

        mejor_match = None
        for _, cand in candidatos.iterrows():
            if cand['Nº de anomalia'] in ids_asignados: continue

            vano_i = cand.get('VANO_NORM', '')
            if vano_c and vano_i:
                coincide_vano = (vano_c == vano_i)
                if not coincide_vano and '-' in vano_c:
                    partes = vano_c.split('-')
                    if len(partes) == 2 and f"{partes[1]}-{partes[0]}" == vano_i: coincide_vano = True
                if not coincide_vano: continue

            cand_dist_num = cand.get('DIST_CALC')
            if pd.notna(dist_c_num) and pd.notna(cand_dist_num) and abs(dist_c_num - cand_dist_num) > 0.5: continue

            mejor_match = cand
            ids_asignados.add(cand['Nº de anomalia'])
            break

        fila_res = row_c.to_dict()

        if mejor_match is not None:
            fila_res['Nº de anomalia'] = mejor_match['Nº de anomalia']
            fila_res['ID_Original_Informe'] = mejor_match['ID_ANOMALIA']

            desc_final = fila_res.get(col_desc_comb, "") if col_desc_comb else ""
            if pd.isna(desc_final) or str(desc_final).strip() == "":
                col_desc_inf = next((c for c in mejor_match.keys() if
                                     any(p in str(c).lower() for p in ['descrip', 'observaci', 'texto', 'defecto'])),
                                    None)
                if col_desc_inf: desc_final = mejor_match[col_desc_inf]
            fila_res['Descripción'] = desc_final if pd.notna(desc_final) else ""

            # Rescatamos variables mapeadas por el diccionario
            for k in cols_tecnicas:
                val = mejor_match.get(k)
                if pd.notna(val) and str(val).strip() != "":
                    fila_res[k] = val


            # pillamos distancia apoyo
            if pd.isna(fila_res.get('DIST_APOYO')) or str(fila_res.get('DIST_APOYO')).strip() == "":
                for col_name in mejor_match.keys():
                    col_str = str(col_name).lower()
                    if 'distancia' in col_str and 'apoyo' in col_str:
                        val_apoyo = mejor_match[col_name]
                        if pd.notna(val_apoyo) and str(val_apoyo).strip() != "":
                            fila_res['DIST_APOYO'] = val_apoyo
                            break

            # pillamos Temperatura
            if pd.isna(fila_res.get('TEMP_MAX')) or str(fila_res.get('TEMP_MAX')).strip() == "":
                for col_name in mejor_match.keys():
                    col_str = str(col_name).lower()
                    if 'temp' in col_str:
                        val_temp = mejor_match[col_name]
                        if pd.notna(val_temp) and str(val_temp).strip() != "":
                            fila_res['TEMP_MAX'] = val_temp
                            break

        else:
            fila_res['Nº de anomalia'] = None
            fila_res['ID_Original_Informe'] = None
            desc_final = fila_res.get(col_desc_comb, "") if col_desc_comb else ""
            fila_res['Descripción'] = desc_final if pd.notna(desc_final) else ""

        # Vano y Circuito sin vacios
        if col_vano_c and (pd.isna(fila_res.get('VANO')) or str(fila_res.get('VANO')).strip() == ""):
            fila_res['VANO'] = row_c.get(col_vano_c)
        if col_cir_c and (pd.isna(fila_res.get('CIRCUITO')) or str(fila_res.get('CIRCUITO')).strip() == ""):
            fila_res['CIRCUITO'] = row_c.get(col_cir_c)

        filas_finales.append(fila_res)

    builder_instance.product.data_dt = pd.DataFrame(filas_finales)
    info(f"Paso 3 terminado. {len(ids_asignados)} anomalias vinculadas de forma exitosa")