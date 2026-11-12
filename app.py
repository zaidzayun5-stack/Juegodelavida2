import random
import streamlit as st

st.set_page_config(page_title="Juego de la Vida", page_icon="🧬", layout="wide")

# -------------------- LÓGICA DEL AUTÓMATA --------------------
def crear_tablero(filas: int, columnas: int) -> list[list[int]]:
    return [[0 for _ in range(columnas)] for _ in range(filas)]


def contar_vecinas(tablero: list[list[int]], fila: int, columna: int) -> int:
    filas, columnas = len(tablero), len(tablero[0])
    total = 0

    for df in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if df == 0 and dc == 0:
                continue

            nueva_fila = fila + df
            nueva_columna = columna + dc

            # Los bordes no se conectan entre sí: fuera del tablero no hay células.
            if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
                total += tablero[nueva_fila][nueva_columna]

    return total


def siguiente_generacion(tablero: list[list[int]]) -> list[list[int]]:
    filas, columnas = len(tablero), len(tablero[0])
    nuevo = crear_tablero(filas, columnas)

    for fila in range(filas):
        for columna in range(columnas):
            vecinas = contar_vecinas(tablero, fila, columna)
            viva = tablero[fila][columna] == 1

            if viva and vecinas in (2, 3):
                nuevo[fila][columna] = 1
            elif not viva and vecinas == 3:
                nuevo[fila][columna] = 1
            else:
                nuevo[fila][columna] = 0

    return nuevo


def tablero_aleatorio(filas: int, columnas: int, probabilidad: float = 0.25):
    return [
        [1 if random.random() < probabilidad else 0 for _ in range(columnas)]
        for _ in range(filas)
    ]


def contar_vivas(tablero: list[list[int]]) -> int:
    return sum(sum(fila) for fila in tablero)


# -------------------- ESTADO DE LA APLICACIÓN --------------------
if "filas" not in st.session_state:
    st.session_state.filas = 20
    st.session_state.columnas = 30
    st.session_state.tablero = crear_tablero(20, 30)
    st.session_state.generacion = 0
    st.session_state.ejecutando = False

st.title("🧬 Juego de la Vida de Conway")
st.write(
    "Un autómata celular: cada célula vive, muere o nace según la cantidad "
    "de vecinas vivas que tiene."
)

with st.sidebar:
    st.header("Configuración")
    nuevas_filas = st.slider("Filas", 8, 30, st.session_state.filas)
    nuevas_columnas = st.slider("Columnas", 8, 40, st.session_state.columnas)
    densidad = st.slider("Densidad aleatoria", 0.05, 0.60, 0.25, 0.05)

    if (nuevas_filas, nuevas_columnas) != (
        st.session_state.filas,
        st.session_state.columnas,
    ):
        st.session_state.filas = nuevas_filas
        st.session_state.columnas = nuevas_columnas
        st.session_state.tablero = crear_tablero(nuevas_filas, nuevas_columnas)
        st.session_state.generacion = 0
        st.session_state.ejecutando = False
        st.rerun()

    st.caption("Los bordes del tablero se consideran límites: no hay conexión entre extremos.")

# -------------------- CONTROLES --------------------
c1, c2, c3, c4 = st.columns(4)

if c1.button("▶️ Iniciar" if not st.session_state.ejecutando else "⏸️ Pausar", use_container_width=True):
    st.session_state.ejecutando = not st.session_state.ejecutando
    st.rerun()

if c2.button("⏭️ Siguiente generación", use_container_width=True):
    st.session_state.ejecutando = False
    st.session_state.tablero = siguiente_generacion(st.session_state.tablero)
    st.session_state.generacion += 1
    st.rerun()

if c3.button("🎲 Aleatorio", use_container_width=True):
    st.session_state.ejecutando = False
    st.session_state.tablero = tablero_aleatorio(
        st.session_state.filas, st.session_state.columnas, densidad
    )
    st.session_state.generacion = 0
    st.rerun()

if c4.button("🧹 Limpiar", use_container_width=True):
    st.session_state.ejecutando = False
    st.session_state.tablero = crear_tablero(
        st.session_state.filas, st.session_state.columnas
    )
    st.session_state.generacion = 0
    st.rerun()

# -------------------- EVOLUCIÓN AUTOMÁTICA --------------------
# El fragmento se actualiza periódicamente mientras el modo automático está activo.
@st.fragment(run_every=0.5 if st.session_state.ejecutando else None)
def mostrar_tablero():
    if st.session_state.ejecutando:
        st.session_state.tablero = siguiente_generacion(st.session_state.tablero)
        st.session_state.generacion += 1

    vivas = contar_vivas(st.session_state.tablero)
    m1, m2, m3 = st.columns(3)
    m1.metric("Generación", st.session_state.generacion)
    m2.metric("Células vivas", vivas)
    m3.metric("Células muertas", st.session_state.filas * st.session_state.columnas - vivas)

    st.subheader("Tablero")
    st.caption("Haz clic en una celda para cambiarla entre viva y muerta.")

    # Cada botón representa una célula. El color/emoji permite distinguir sus estados.
    for fila in range(st.session_state.filas):
        celdas = st.columns(st.session_state.columnas, gap="small")
        for columna in range(st.session_state.columnas):
            viva = st.session_state.tablero[fila][columna] == 1
            etiqueta = "🟩" if viva else "⬛"
            if celdas[columna].button(
                etiqueta,
                key=f"celda_{fila}_{columna}",
                help=f"Fila {fila + 1}, columna {columna + 1}: {'viva' if viva else 'muerta'}",
                use_container_width=True,
            ):
                st.session_state.ejecutando = False
                st.session_state.tablero[fila][columna] = 0 if viva else 1
                st.rerun()

mostrar_tablero()

st.divider()
st.subheader("Reglas del Juego de la Vida")
st.markdown(
    """
    1. **Soledad:** una célula viva con menos de 2 vecinas vivas muere.
    2. **Supervivencia:** una célula viva con 2 o 3 vecinas vivas permanece viva.
    3. **Sobrepoblación:** una célula viva con más de 3 vecinas vivas muere.
    4. **Nacimiento:** una célula muerta con exactamente 3 vecinas vivas nace.
    """
)
st.info(
    "La nueva generación se calcula usando el tablero anterior completo. "
    "Así se evita que el orden de recorrido altere el resultado."
)
