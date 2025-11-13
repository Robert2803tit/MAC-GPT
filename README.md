# MAC-GPT-PROYECTO

Proyecto ETL (Extract, Transform, Load) para la extracción y procesamiento de datos del plan de estudios de la carrera de Matemáticas Aplicadas y Computación de la FES Acatlán, incluyendo un chatbot (MAC-GPT) para consultar información sobre la carrera.

## Estructura del Proyecto

```
proyecto-examen/
│
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuraciones globales, rutas, claves API
│
├── data/                      # Directorio para datos
│   ├── pdfs/                  # PDFs descargados
│   ├── output/                # Archivos de salida (JSON, CSV)
│   └── pickles/               # Archivos pickle de pandas con embeddings
│
├── src/                       # Código fuente
│   ├── chatbot/               # Módulos del chatbot MAC-GPT
│   │   ├── mac_gpt.py         # Implementación del chatbot
│   │   ├── cli.py             # Interfaz de línea de comandos
│   │   └── ejemplo_uso.py     # Ejemplo de uso programático
│   │
│   ├── extractors/            # Módulos para extracción de datos
│   │   ├── web_scraper.py     # Funciones de web scraping
│   │   └── pdf_extractor.py   # Funciones de extracción de PDF
│   │
│   ├── transformers/          # Módulos para transformación de datos
│   │   └── embeddings.py      # Generación de embeddings
│   │
│   └── loaders/               # Módulos para carga de datos
│       └── file_handler.py    # Manejo de archivos locales
│
├── pipeline/                  # Scripts principales para ejecutar el ETL
│   ├── extract.py             # Script para la fase de extracción
│   └── transform.py           # Script para la fase de transformación
│
├── main.py                    # Punto de entrada principal
├── requirements.txt           # Dependencias del proyecto
└── env.example                # Ejemplo de archivo de variables de entorno
```

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`
- API Key de Google Gemini para la generación de embeddings y uso del chatbot

## Instalación

1. Clonar el repositorio:
   ```
   git clone <url-del-repositorio>
   cd proyecto-examen
   ```

2. Crear un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno:
   ```
   cp env.example .env
   ```
   Edita el archivo `.env` para agregar tu API Key de Google Gemini.

## Uso

### Proceso ETL completo

Para ejecutar todo el proceso ETL:

```
python main.py
```

Opciones:
- `--skip-download`: Omitir la descarga de PDFs y usar los existentes
- `--skip-extraction`: Omitir la extracción de datos de los PDFs
- `--skip-embeddings`: No generar embeddings para los datos
- `--pdf-dir PATH`: Directorio donde se encuentran o guardarán los PDFs
- `--output-name NAME`: Nombre base para los archivos de salida

### Chatbot MAC-GPT

Para ejecutar el chatbot MAC-GPT en modo consola:

```
python main.py --chatbot
```

También puede ejecutarse directamente:

```
python -m src.chatbot.cli
```

#### Interfaz Web del Chatbot

El chatbot también cuenta con una interfaz web estilo ChatGPT con modo claro/oscuro:

```
python main.py --web
```

Para opciones adicionales:

```
python main.py --web --port 8080 --debug
```

También puede iniciar la interfaz web directamente:

```
python -m src.chatbot.web.run
```

#### Uso programático del chatbot:

```python
from src.chatbot import configure_google_api, ask_mac_gpt

# Configurar la API (requiere una API key de Google Gemini)
configure_google_api("TU_API_KEY")

# Realizar una consulta al chatbot
respuesta = ask_mac_gpt("¿Cuáles son las áreas de especialización de MAC?")
print(respuesta)
```

Para ver un ejemplo completo, consultar el archivo `src/chatbot/ejemplo_uso.py`.

### Ejecución por fases

#### Solo extracción:

```
python -m pipeline.extract
```

Opciones:
- `--skip-download`: Omitir la descarga de PDFs
- `--skip-extraction`: Omitir la extracción de datos
- `--pdf-dir PATH`: Directorio de PDFs
- `--output-name NAME`: Nombre base para los archivos de salida

#### Solo transformación:

```
python -m pipeline.transform --input-file data/pickles/tu_archivo.pkl
```

Opciones:
- `--no-embeddings`: No generar embeddings
- `--text-columns COL1 COL2`: Columnas específicas para generar embeddings
- `--output-name NAME`: Nombre base para el archivo de salida
- `--output-format {pickle,csv,both}`: Formato de salida

## Flujo de Datos

1. **Extracción**: 
   - Descarga PDFs del sitio web de la FES Acatlán
   - Extrae información estructurada de los PDFs usando Google Gemini API

2. **Transformación**:
   - Limpieza y normalización de datos
   - Generación de embeddings para búsqueda semántica

3. **Carga**: 
   - Almacenamiento de datos en formatos CSV y Pickle
   - Opcionalmente, los datos pueden ser cargados en una base de datos

4. **Chatbot**:
   - Selección de la fuente de datos más relevante para la pregunta
   - Recuperación de contexto basada en similitud de embeddings
   - Generación de respuestas usando Google Gemini API

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. 