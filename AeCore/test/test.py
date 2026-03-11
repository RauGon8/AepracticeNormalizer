import os

from AeCore.AeLogic.AeFacade.facade import AeFacade

# Añadimos la ruta raíz al sistema para encontrar AeCore



#Función para simular la barra de carga en la consola
def imprimir_progreso_consola(porcentaje, mensaje):
    print(f">>> [{porcentaje}%] {mensaje}")


def ejecutar_prueba_real():

    print(" INICIANDO TEST DE BACKEND")


    configuracion_simulada = {
        "rutas_maestras": {
            0: ["C:/Users/Andress/Documents/ENTRADA/COMBINADO/5921_400ARN-CNAV1_Combinado_3.xls"],
            1: ["C:/Users/Andress/Documents/ENTRADA/H2","C:/Users/Andress/Documents/ENTRADA\H2-1","C:/Users/Andress/Documents/ENTRADA/H3","C:/Users/Andress/Documents/ENTRADA/H3-0"],
            2: ["C:/Users/Andress/Documents/ENTRADA/TablaAgrupacionPorteman.xls"],
            3: ["C:/Users/Andress/Documents/ENTRADA/info_vanos/5921_400ARN-CNAV1.xls"]
        },
        "carpeta_salida": "C:/Users/Andress/Documents/pruebas",
        "orden_trabajo": "809999"
    }

    #validamos rapido que la carpeta de salida exista, si no la creamos
    os.makedirs(configuracion_simulada["carpeta_salida"], exist_ok=True)

    #instanciamos la puerta de entrada (Facade)
    facade = AeFacade()

    try:
        #rjecutamos todo el proceso pasándole la configuración y nuestra función de imprimir
        producto_final = facade.run_full_process(
            config=configuracion_simulada,
            progress_callback=imprimir_progreso_consola
        )

        print("=" * 50)
        print(" TEST COMPLETADO CON ÉXITO ")
        print("=" * 50)

        #cmprobamos qué ha devuelto la caja final
        dataframe_final = producto_final.data_dt
        if not dataframe_final.empty:
            print(f"Total de anomalías procesadas: {len(dataframe_final)} filas.")
            print(f"Columnas resultantes: {list(dataframe_final.columns)}")
            print(f"Revisa tu carpeta de salida: {configuracion_simulada['carpeta_salida']}")
        else:
            print("El proceso terminó pero la tabla final está vacía.")

    except Exception as e:
        print("\n" + "=" * 50)
        print(" ERROR FATAL DURANTE EL TEST ")
        print("=" * 50)
        print(f"Motivo del fallo: {str(e)}")


if __name__ == "__main__":
    ejecutar_prueba_real()