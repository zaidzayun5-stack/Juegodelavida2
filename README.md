# Juego de la Vida de Conway

Implementación del autómata celular de John Horton Conway con **Python y Streamlit**. Tanto la lógica como la interfaz están escritas en Python.

## Funcionalidades

- Tablero interactivo: clic en una celda para cambiar su estado.
- Inicio y pausa de la simulación automática.
- Avance manual de una generación.
- Generación aleatoria de células.
- Limpieza del tablero.
- Configuración del tamaño y densidad inicial.
- Contador de generaciones y población viva/muerta.

## Requisitos

- Python 3.10 o superior.
- pip.

## Ejecutar localmente

```bash
# 1. Crear y activar un entorno virtual (opcional, pero recomendado)
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá en el navegador, normalmente en `http://localhost:8501`.

## Publicar en Streamlit Community Cloud

1. Crea un repositorio público en GitHub.
2. Sube `app.py`, `requirements.txt`, `README.md` y `.gitignore`.
3. Entra a [Streamlit Community Cloud](https://share.streamlit.io/).
4. Inicia sesión con GitHub y autoriza el acceso al repositorio.
5. Selecciona **Create app**, el repositorio, la rama `main` y el archivo `app.py`.
6. Pulsa **Deploy**.

## Reglas del autómata

Para cada célula se cuentan las ocho posiciones vecinas:

- Una célula viva con menos de dos vecinas vivas muere.
- Una célula viva con dos o tres vecinas vivas sobrevive.
- Una célula viva con más de tres vecinas vivas muere.
- Una célula muerta con exactamente tres vecinas vivas nace.

Los límites del tablero se consideran bordes cerrados: las posiciones fuera de la cuadrícula no cuentan como vecinas.

## Estructura

```text
juego-vida-conway/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
