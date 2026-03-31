# Rec_script_to_Rpp

Herramienta en Python para convertir un **script de grabación** (Excel/CSV) y una carpeta de audios `.wav` en un proyecto de **REAPER** (`.rpp`) con ítems posicionados automáticamente.

## ¿Qué hace?

- Lee un archivo de script de grabación (`.xlsx`, `.xls` o `.csv`).
- Busca archivos `.wav` en una carpeta (incluye subcarpetas).
- Asocia cada nombre de archivo del script con su ruta de audio real.
- Calcula la duración de cada audio y una posición temporal para cada ítem.
- Genera:
  - un archivo de apoyo `Dataframe_<script>.xlsx` con los datos procesados,
  - un proyecto de REAPER `.rpp` listo para abrir.

## Componentes del proyecto

- `main.py`: interfaz gráfica (CustomTkinter) para ejecutar el flujo.
- `backend.py`: lógica principal para validaciones, dataframe y generación del `.rpp`.
- `backend_no_gui.py`: variante por consola (sin interfaz gráfica).
- `lib_installer.py`: instalador/verificador de dependencias de `requirements.txt`.
- `requirements.txt`: librerías necesarias.

## Requisitos

- Python 3.10+ (recomendado 3.12 o menor si usas `pydub`).
- Dependencias del archivo `requirements.txt`.

## Instalación

1. Clona o descarga este repositorio.
2. (Opcional) Crea y activa un entorno virtual.
3. Instala dependencias:

```bash
pip install -r requirements.txt
```

## Uso (interfaz gráfica)

Ejecuta:

```bash
python main.py
```

En la ventana, completa:

1. **Script file path**: ruta del archivo de script (`.xlsx`, `.xls`, `.csv`).
2. **Audio file location**: carpeta donde están los audios `.wav`.
3. **Sample rate**: `44100`, `48000` o `96000`.
4. **Filename column**: nombre de la columna con nombres de archivo de audio (ej. `line_001.wav`).
5. **Item notes column**: nombre de la columna con el texto/notas para cada ítem.

Luego presiona **Generate**.

## Uso (modo consola)

Ejecuta:

```bash
python backend_no_gui.py
```

Sigue los prompts para indicar rutas, columnas y sample rate.

## Salida esperada

En el mismo directorio del script original se generan:

- `Dataframe_<nombre_script>.xlsx`
- `<nombre_script>.rpp`

## Notas

- La búsqueda de audios es por nombre de archivo exacto.
- Si algún audio no se encuentra, el dataframe marca `Not Found`.
- Las posiciones se asignan secuencialmente con separación fija de 4 segundos entre ítems.

## Posibles problemas

- **“Header not in file”**: revisa que el nombre de columna coincida exactamente.
- **Ruta inválida**: verifica comillas, espacios y que el archivo/carpeta exista.
- **Dependencias faltantes**: reinstala con `pip install -r requirements.txt`.

## Licencia

Este proyecto no incluye licencia explícita por el momento.
