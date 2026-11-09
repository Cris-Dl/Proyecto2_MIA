# Proyecto2_MIA

[![Ver Informe Técnico](https://img.shields.io/badge/Ver_Informe_Técnico-PDF-red?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](./docs/Proyecto02_MIA.pdf)

Este proyecto es una aplicación de escritorio desarrollada en Python que implementa un sistema de gestión de contactos utilizando archivos de texto con registros de longitud fija (126 bytes) y acceso aleatorio mediante punteros (`seek` y `tell`).

El proyecto fue desarrollado para el curso de Manejo e Implementación de Archivos de la Universidad Rafael Landívar.

##  Características Principales

*   **Acceso Aleatorio (O(1)):** Lectura y modificación *in-place* directa en el disco sin recorrer el archivo secuencialmente.
*   **Índice en Memoria:** Utiliza un archivo JSON secundario para mapear IDs lógicos a posiciones físicas de manera ultra rápida.
*   **Seguridad e Integridad:** Verificación criptográfica con **SHA-256** para detectar si la base de datos fue alterada de forma externa.
*   **Interfaz Gráfica Moderna:** UI responsiva con modo claro/oscuro construida con **NiceGUI**.
*   **Exportación y Respaldo:** Generación de reportes tabulares en **PDF**, exportación estructurada en **JSON** y compresión en formato **ZIP**.

##  Requisitos Previos

Para ejecutar este proyecto, necesitas tener instalado en tu sistema:
*   [Python 3.8](https://www.python.org/downloads/) o superior.
*   Gestor de paquetes `pip`.

##  Instalación y Configuración

Sigue estos pasos en tu terminal para hacer funcionar el programa localmente:

1. **Clonar el repositorio:**
   ```bash
   git clone <https://github.com/Cris-Dl/Proyecto2_MIA.git>
   cd Proyecto2_MIA
   ```

2. **Crear y activar un entorno virtual (Recomendado):**
   * En Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * En macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar las dependencias requeridas:**
   El proyecto utiliza `nicegui` para la interfaz y `reportlab` para la generación de PDFs.
   ```bash
   pip install nicegui reportlab
   ```

##  Ejecución del Programa

Una vez instaladas las dependencias, simplemente ejecuta el archivo principal ubicado en la carpeta fuente:

```bash
python src/main.py
```

La aplicación se abrirá automáticamente en una ventana de escritorio independiente.

##  Estructura del Proyecto

```text
Proyecto2_MIA/
│
├── data/                   # Base de datos (Ignorada parcialmente en Git)
│   ├── contactos.dat       # Archivo principal (longitud fija 126 bytes)
│   ├── indice.json         # Diccionario en memoria (ID -> Posición)
│   └── contactos.sha256    # Hash de seguridad
│
├── docs/                   # Documentación
│   └── Proyecto02_MIA.pdf  # Reporte técnico final
│
├── reports/                # Archivos generados por el usuario
│   ├── exportacion.json
│   ├── reporte_contactos.pdf
│   └── respaldo_agenda.zip
│
└── src/                    # Código fuente Python
    ├── main.py             # Punto de entrada
    ├── interfaz.py         # Interfaz gráfica (NiceGUI)
    ├── repositorio_archivos.py # Backend CRUD con seek/tell
    ├── gestor_indice.py    # Lógica del diccionario
    ├── utilidades.py       # Hashing y Backups ZIP
    └── exportador.py       # Generación de PDF y JSON
```

---
**Desarrollado por:** Cristhian Estuardo De León Pérez
