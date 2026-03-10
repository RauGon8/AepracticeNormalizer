<div align="center">

# AePracticeNormalizer (AeTools)

[![Python 3](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)]()
[![PySide6](https://img.shields.io/badge/PySide6-GUI-41CD52.svg?style=for-the-badge&logo=qt&logoColor=white)]()
[![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)]()
[![Openpyxl](https://img.shields.io/badge/Openpyxl-Excel-ff69b4.svg?style=for-the-badge)]()

*Automatización, procesamiento asíncrono y normalización de datos masivos para infraestructuras.*

</div>

<br />

## 📑 Tabla de Contenidos
- [Descripción General](#-descripción-general)
- [Características y Arquitectura](#️-características-y-arquitectura)
- [Estructura del Proyecto](#-estructura-del-proyecto)


---

## 📌 Descripción General

**AePracticeNormalizer** es una solución de escritorio desarrollada en Python 3 para la automatización, procesamiento y normalización de datos. 
Adicionalmente, garantiza la trazabilidad estructural al vincular y renombrar automáticamente las evidencias gráficas asociadas a cada registro.

---

## ⚙️ Características y Arquitectura

El sistema ha sido construido bajo principios de Ingeniería de Software, implementando patrones de diseño creacionales y de comportamiento para cumplir con los siguientes requisitos técnicos:

* **Interfaz gráfica oscura:** Diseño ergonómico implementado en PySide6, cuya gestión visual y paleta de colores oscuros se centraliza dinámicamente a través del módulo `ThemeManager`.
* **Patrón de diseño Builder:** La lógica de procesamiento secuencial está estructurada mediante los patrones `Builder`, `Director` y `Facade`, logrando un desacoplamiento total entre la construcción de los datos complejos y su representación.
* **Patrón Strategy:** La exportación de datos a `.xls` se realiza mediante una interfaz polimórfica (`XlsExporter`), permitiendo la ejecución de estrategias concretas (ej. `LiteExporter`, `Exporter2026`) según las necesidades del formato de salida, respetando el principio Abierto/Cerrado (OCP).
* **Ejecución asíncrona:** La arquitectura emplea concurrencia a través de `QThread`, delegando el procesamiento intensivo de datos a un hilo secundario para prevenir el congelamiento de la interfaz de usuario (UI).
* **QDialog modal nativo:** El reporte de progreso del subproceso se expone mediante un componente `QDialog` estrictamente modal, el cual bloquea la interacción del usuario con la ventana principal hasta la culminación de la tarea.
* **Alto rendimiento:** El uso de operaciones vectorizadas en memoria a través de la biblioteca Pandas garantiza tiempos de ejecución sistemáticamente inferiores a los 20 segundos para el flujo completo del script.
* **Entorno de pruebas headless:** El repositorio incluye un directorio `test` diseñado para la ejecución secuencial y validación del backend sin necesidad de instanciar la interfaz gráfica de PySide6.
* **Persistencia nativa:** El almacenamiento de los ajustes de usuario (rutas de trabajo, configuración visual, etc.) se gestiona utilizando `QSettings`, garantizando una integración nativa y persistente con el registro del sistema operativo.
* **Sistema de logging:** La trazabilidad operativa se encuentra cubierta por el módulo `aelogging`, encargado de registrar el flujo de ejecución y documentar excepciones a lo largo de toda la arquitectura.

---

## 📂 Estructura del Proyecto

La base de código respeta una separación estricta de responsabilidades (Presentación, Lógica de Negocio y Pruebas), organizada de la siguiente manera:

```text
AepracticeNormalizer/
├── AeCore/                         # Capa de Lógica de Negocio y Datos
│   ├── AeLogic/                    # Motor central y Patrones de Diseño
│   │   ├── AeBuilder/              # Construcción secuencial
│   │   │   ├── builder.py          # Implementación del Patrón Builder
│   │   │   ├── director.py         # Orquestador (Patrón Director)
│   │   │   └── steep1.py a steep6.py # Pasos lógicos (Paso 6 incluye Patrón Strategy)
│   │   └── AeFacade/               # Puerta de enlace unificada
│   │       └── facade.py           # Implementación del Patrón Facade
│   ├── AeUtils/                    # Herramientas y utilidades transversales
│   │   ├── Aeutils.py              # Funciones de normalización de datos
│   │   └── settings_manager.py     # Gestión de persistencia (QSettings)
│   └── Worker/                     # Gestión de concurrencia
│       └── Worker.py               # Ejecución en hilo secundario (QThread)
├── AeView/                         # Capa de Presentación (Frontend)
│   ├── Forms/                      # Archivos de diseño base de UI
│   ├── Style/                      # Configuración visual y ThemeManager
│   ├── Ui/                         # Interfaces compiladas autogeneradas
│   └── Widgets/                    # Controladores de la interfaz gráfica y Modales
│       ├── main_window.py          # Script principal y punto de entrada de la UI
│       └── settings.py             # Lógica del panel de configuración
├── test/                           # Entorno aislado para pruebas
│   └── test_headless.py            # Ejecución del backend sin UI
└── requirements.txt                # Listado de dependencias del entorno
