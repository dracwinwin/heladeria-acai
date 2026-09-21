"""
🍧 Sistema Financiero - Heladería de Açaí Cobija
App Streamlit TODO-EN-UNO. Datos persistidos en ./data/*.csv
Ejecutar: streamlit run app.py
"""
import os
from datetime import date

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# CONFIGURACIÓN GLOBAL
# =========================================================
st.set_page_config(
    page_title="🍧 Heladería Açaí - Cobija",
    page_icon="🍧",
    layout="wide",
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


# =========================================================
# DATOS SEED (valores iniciales)
# =========================================================
def seed_productos():
    return pd.DataFrame([
        {"codigo": "A1", "producto": "Açaí Pequeño (200ml)", "categoria": "Açaí Tradicional", "precio": 10.0, "costo": 9.0},
        {"codigo": "A2", "producto": "Açaí Mediano (300ml)", "categoria": "Açaí Tradicional", "precio": 20.0, "costo": 14.0},
        {"codigo": "A3", "producto": "Açaí Grande (400ml)", "categoria": "Açaí Tradicional", "precio": 25.0, "costo": 17.0},
        {"codigo": "A4", "producto": "Açaí Especial Premium", "categoria": "Especialidades", "precio": 30.0, "costo": 19.5},
        {"codigo": "B1", "producto": "Jugo Natural de Açaí", "categoria": "Bebidas", "precio": 12.0, "costo": 7.0},
    ])

def seed_ventas():
    return pd.DataFrame(columns=["n_trans", "fecha", "producto", "cantidad"])

def seed_costos_fijos():
    return pd.DataFrame([
        {"categoria": "Alquiler del Local", "descripcion": "Local céntrico en Cobija", "monto": 2500.0},
        {"categoria": "Servicios Básicos", "descripcion": "ENDE / EPSA Cobija", "monto": 900.0},
        {"categoria": "Sueldos de Personal", "descripcion": "1 Admin + 1 Auxiliar", "monto": 4500.0},
        {"categoria": "Internet y Telefonía", "descripcion": "Fibra óptica", "monto": 250.0},
        {"categoria": "Mantenimiento", "descripcion": "Revisión congeladores", "monto": 300.0},
        {"categoria": "Limpieza e Higiene", "descripcion": "Desinfectantes", "monto": 200.0},
        {"categoria": "Publicidad", "descripcion": "Redes y volantes", "monto": 350.0},
        {"categoria": "Patente Municipal", "descripcion": "Impuestos", "monto": 200.0},
    ])

def seed_bom():
    return pd.DataFrame([
        {"componente": "Base de Açaí", "detalle": "Pulpa congelada", "cantidad": "150 gr", "costo": 8.0},
        {"componente": "Fruta Fresca", "detalle": "Plátano, frutilla, kiwi", "cantidad": "80 gr", "costo": 2.0},
        {"componente": "Toppings", "detalle": "Granola, leche", "cantidad": "40 gr", "costo": 2.0},
        {"componente": "Envase y Desechables", "detalle": "Vaso + tapa + cuchara", "cantidad": "1 unid", "costo": 1.0},
        {"componente": "Insumos Secundarios", "detalle": "Servilletas y energía", "cantidad": "1 serv", "costo": 1.0},
    ])

def seed_encuestas():
    """Encuestas pre-cargadas del Excel original."""
    filas = [
        # P1
        ("P1. ¿Con qué frecuencia compras en la heladería?", "Diario", 15),
        ("P1. ¿Con qué frecuencia compras en la heladería?", "2-3 veces por semana", 45),
        ("P1. ¿Con qué frecuencia compras en la heladería?", "Semanal", 25),
        ("P1. ¿Con qué frecuencia compras en la heladería?", "Ocasional", 15),
        # P2
        ("P2. ¿Cuál es tu producto favorito de açaí?", "Açaí Mediano Tradicional", 42),
        ("P2. ¿Cuál es tu producto favorito de açaí?", "Açaí Especial Premium", 28),
        ("P2. ¿Cuál es tu producto favorito de açaí?", "Açaí Pequeño", 18),
        ("P2. ¿Cuál es tu producto favorito de açaí?", "Jugo de Açaí", 12),
        # P3
        ("P3. ¿Qué tamaño prefieres habitualmente?", "Mediano (350ml)", 50),
        ("P3. ¿Qué tamaño prefieres habitualmente?", "Grande (500ml)", 25),
        ("P3. ¿Qué tamaño prefieres habitualmente?", "Pequeño (200ml)", 20),
        ("P3. ¿Qué tamaño prefieres habitualmente?", "Familiar / Especial", 5),
        # P4
        ("P4. ¿Consideras adecuados los precios actuales?", "Muy adecuados", 35),
        ("P4. ¿Consideras adecuados los precios actuales?", "Adecuados", 52),
        ("P4. ¿Consideras adecuados los precios actuales?", "Elevados", 10),
        ("P4. ¿Consideras adecuados los precios actuales?", "Muy elevados", 3),
        # P5
        ("P5. ¿Qué toppings prefieres agregar a tu açaí?", "Fruta fresca (Frutilla/Plátano)", 38),
        ("P5. ¿Qué toppings prefieres agregar a tu açaí?", "Granola y Cereales", 27),
        ("P5. ¿Qué toppings prefieres agregar a tu açaí?", "Leche condensada / en polvo", 23),
        ("P5. ¿Qué toppings prefieres agregar a tu açaí?", "Frutos secos / Chocolates", 12),
        # P6
        ("P6. ¿Cuánto pagarías por un nuevo combo?", "Bs 15 - Bs 20", 25),
        ("P6. ¿Cuánto pagarías por un nuevo combo?", "Bs 20 - Bs 25", 48),
        ("P6. ¿Cuánto pagarías por un nuevo combo?", "Bs 25 - Bs 35", 22),
        ("P6. ¿Cuánto pagarías por un nuevo combo?", "Más de Bs 35", 5),
        # P7
        ("P7. ¿En qué horario sueles comprar más?", "Tarde (14:00 - 18:00)", 45),
        ("P7. ¿En qué horario sueles comprar más?", "Noche (18:00 - 22:00)", 40),
        ("P7. ¿En qué horario sueles comprar más?", "Mañana (09:00 - 12:00)", 10),
        ("P7. ¿En qué horario sueles comprar más?", "Mediodía (12:00 - 14:00)", 5),
        # P8
        ("P8. ¿Qué te motiva a elegir esta heladería?", "Calidad y sabor del açaí", 52),
        ("P8. ¿Qué te motiva a elegir esta heladería?", "Ubicación céntrica en Cobija", 20),
        ("P8. ¿Qué te motiva a elegir esta heladería?", "Atención al cliente", 18),
        ("P8. ¿Qué te motiva a elegir esta heladería?", "Precios competitivos", 10),
        # P9
        ("P9. ¿Qué producto nuevo te gustaría?", "Açaí Batido Protein", 35),
        ("P9. ¿Qué producto nuevo te gustaría?", "Waffles con Açaí", 30),
        ("P9. ¿Qué producto nuevo te gustaría?", "Helado Keto Sin Azúcar", 20),
        ("P9. ¿Qué producto nuevo te gustaría?", "Smoothies Tropicales", 15),
        # P10
        ("P10. ¿Recomendarías la heladería?", "Definitivamente sí", 78),
        ("P10. ¿Recomendarías la heladería?", "Probablemente sí", 18),
        ("P10. ¿Recomendarías la heladería?", "Tal vez", 3),
        ("P10. ¿Recomendarías la heladería?", "No", 1),
    ]
    return pd.DataFrame(filas, columns=["pregunta", "opcion", "respuestas"])

def seed_prediccion():
    return pd.DataFrame([
        {"mes_num": 1, "mes": "Septiembre 2026", "tipo": "Histórico Real", "unidades": 450, "precio_prom": 19.5},
        {"mes_num": 2, "mes": "Octubre 2026", "tipo": "Histórico Real", "unidades": 500, "precio_prom": 19.5},
        {"mes_num": 3, "mes": "Noviembre 2026", "tipo": "Histórico Real", "unidades": 550, "precio_prom": 19.8},
        {"mes_num": 4, "mes": "Diciembre 2026", "tipo": "Proyección", "unidades": 620, "precio_prom": 20.0},
        {"mes_num": 5, "mes": "Enero 2027", "tipo": "Proyección", "unidades": 670, "precio_prom": 20.0},
        {"mes_num": 6, "mes": "Febrero 2027", "tipo": "Proyección", "unidades": 720, "precio_prom": 20.0},
    ])


# =========================================================
# PERSISTENCIA CSV
# =========================================================
def _path(nombre):
    return os.path.join(DATA_DIR, f"{nombre}.csv")

def cargar_o_crear(nombre, seed_fn):
    p = _path(nombre)
    if os.path.exists(p):
        try:
            return pd.read_csv(p)
        except Exception:
            return seed_fn()
    df = seed_fn()
    df.to_csv(p, index=False)
    return df

def guardar(nombre, df):
    df.to_csv(_path(nombre), index=False)

def init_state():
    if "df_productos" not in st.session_state:
        st.session_state.df_productos = cargar_o_crear("productos", seed_productos)
    if "df_ventas" not in st.session_state:
        st.session_state.df_ventas = cargar_o_crear("ventas", seed_ventas)
    if "df_costos_fijos" not in st.session_state:
        st.session_state.df_costos_fijos = cargar_o_crear("costos_fijos", seed_costos_fijos)
    if "df_bom" not in st.session_state:
        st.session_state.df_bom = cargar_o_crear("bom", seed_bom)
    if "df_encuestas" not in st.session_state:
        st.session_state.df_encuestas = cargar_o_crear("encuestas", seed_encuestas)
    if "df_prediccion" not in st.session_state:
        st.session_state.df_prediccion = cargar_o_crear("prediccion", seed_prediccion)

def persistir_todo():
    guardar("productos", st.session_state.df_productos)
    guardar("ventas", st.session_state.df_ventas)
    guardar("costos_fijos", st.session_state.df_costos_fijos)
    guardar("bom", st.session_state.df_bom)
    guardar("encuestas", st.session_state.df_encuestas)
    guardar("prediccion", st.session_state.df_prediccion)


# =========================================================
# LÓGICA DE CÁLCULOS
# =========================================================
def enriquecer_ventas(df_ventas, df_productos):
    if df_ventas.empty:
        return pd.DataFrame(columns=[
            "n_trans", "fecha", "producto", "cantidad", "precio_unit",
            "venta_total", "costo_unit", "costo_total", "utilidad_bruta", "margen_pct"
        ])
    df = df_ventas.copy()
    prod = df_productos.set_index("producto")
    df["precio_unit"] = df["producto"].map(prod["precio"]).fillna(0)
    df["costo_unit"] = df["producto"].map(prod["costo"]).fillna(0)
    df["venta_total"] = df["cantidad"] * df["precio_unit"]
    df["costo_total"] = df["cantidad"] * df["costo_unit"]
    df["utilidad_bruta"] = df["venta_total"] - df["costo_total"]
    df["margen_pct"] = np.where(df["venta_total"] > 0,
                                df["utilidad_bruta"] / df["venta_total"], 0)
    return df

def resumen_ventas(df):
    if df.empty:
        return {"unidades": 0, "ingresos": 0.0, "costos": 0.0, "utilidad": 0.0, "margen": 0.0}
    ing = float(df["venta_total"].sum())
    return {
        "unidades": int(df["cantidad"].sum()),
        "ingresos": ing,
        "costos": float(df["costo_total"].sum()),
        "utilidad": float(df["utilidad_bruta"].sum()),
        "margen": float(df["utilidad_bruta"].sum() / ing) if ing > 0 else 0.0,
    }

def ranking_productos(df_enr, df_prod):
    if df_enr.empty:
        return pd.DataFrame()
    agg = df_enr.groupby("producto").agg(
        unidades=("cantidad", "sum"),
        ingresos=("venta_total", "sum"),
        costo=("costo_total", "sum"),
        utilidad=("utilidad_bruta", "sum"),
    ).reset_index()
    agg = agg.merge(df_prod[["producto", "precio"]], on="producto", how="left")
    total = agg["ingresos"].sum()
    agg["participacion"] = agg["ingresos"] / total if total > 0 else 0
    agg = agg.sort_values("ingresos", ascending=False).reset_index(drop=True)
    agg.insert(0, "ranking", agg.index + 1)
    return agg

def predecir_ventas(df_pred):
    df = df_pred.copy()
    historico = df[df["tipo"].str.contains("Histórico", case=False, na=False)]
    if len(historico) >= 2:
        x = historico["mes_num"].values
        y = historico["unidades"].values
        coef = np.polyfit(x, y, 1)
        unidades_aj = []
        for _, row in df.iterrows():
            if row["tipo"] and "Histórico" in str(row["tipo"]):
                unidades_aj.append(row["unidades"])
            else:
                unidades_aj.append(max(0, coef[0] * row["mes_num"] + coef[1]))
        df["unidades_ajustadas"] = np.round(unidades_aj, 0)
    else:
        df["unidades_ajustadas"] = df["unidades"]
    df["ingresos"] = df["unidades_ajustadas"] * df["precio_prom"]
    return df

def costo_variable_unitario(df_bom):
    if df_bom.empty:
        return 0.0
    return float(df_bom["costo"].sum())

def costos_fijos_totales(df_cf):
    if df_cf.empty:
        return 0.0
    return float(df_cf["monto"].sum())

def punto_equilibrio(precio_prom, cvu, cf):
    margen = precio_prom - cvu
    if margen <= 0:
        return {"margen_unit": margen, "pe_unidades": float("inf"), "pe_ingresos": float("inf")}
    pe_u = cf / margen
    return {"margen_unit": margen, "pe_unidades": pe_u, "pe_ingresos": pe_u * precio_prom}

def estado_resultados(ingresos, unidades, cvu, cf):
    cv = unidades * cvu
    mc = ingresos - cv
    ebitda = mc - cf
    return {
        "ingresos": ingresos, "costos_variables": cv,
        "margen_contribucion": mc, "costos_fijos": cf, "ebitda": ebitda,
    }


# =========================================================
# IMPORTADOR CSV/EXCEL
# =========================================================
ESQUEMAS = {
    "productos": ["codigo", "producto", "categoria", "precio", "costo"],
    "ventas": ["n_trans", "fecha", "producto", "cantidad"],
    "costos_fijos": ["categoria", "descripcion", "monto"],
    "bom": ["componente", "detalle", "cantidad", "costo"],
    "encuestas": ["pregunta", "opcion", "respuestas"],
    "prediccion": ["mes_num", "mes", "tipo", "unidades", "precio_prom"],
}

EJEMPLOS = {
    "productos": "codigo,producto,categoria,precio,costo\nA1,Açaí Pequeño,Açaí Tradicional,10,9",
    "ventas": "n_trans,fecha,producto,cantidad\n1,2026-09-01,Açaí Pequeño (200ml),15",
    "costos_fijos": "categoria,descripcion,monto\nAlquiler,Local céntrico,2500",
    "bom": "componente,detalle,cantidad,costo\nBase de Açaí,Pulpa,150 gr,8",
    "encuestas": "pregunta,opcion,respuestas\nP1. Frecuencia,Diario,15",
    "prediccion": "mes_num,mes,tipo,unidades,precio_prom\n1,Septiembre 2026,Histórico Real,450,19.5",
}

def leer_archivo(archivo):
    nombre = archivo.name.lower()
    if nombre.endswith(".csv"):
        try:
            return pd.read_csv(archivo)
        except UnicodeDecodeError:
            archivo.seek(0)
            return pd.read_csv(archivo, encoding="latin-1")
    elif nombre.endswith((".xlsx", ".xls")):
        return pd.read_excel(archivo)
    raise ValueError("Formato no soportado. Usa CSV o Excel.")

def render_importador(clave, etiqueta, estado_key, modo="reemplazar"):
    with st.expander(f"📥 Importar {etiqueta}", expanded=False):
        st.caption(f"**Columnas requeridas:** `{', '.join(ESQUEMAS[clave])}`")
        st.code(EJEMPLOS[clave], language="csv")
        archivo = st.file_uploader(
            f"Sube tu archivo de {etiqueta}",
            type=["csv", "xlsx", "xls"],
            key=f"uploader_{clave}",
        )
        if archivo is not None:
            try:
                df = leer_archivo(archivo)
                faltan = [c for c in ESQUEMAS[clave] if c not in df.columns]
                if faltan:
                    st.error(f"❌ Faltan columnas: {faltan}")
                    return
                st.success(f"✅ {len(df)} filas leídas")
                st.dataframe(df.head(8), use_container_width=True)
                if modo == "reemplazar":
                    if st.button(f"♻️ Reemplazar {etiqueta}", key=f"rep_{clave}"):
                        st.session_state[estado_key] = df
                        st.rerun()
                else:
                    if st.button(f"➕ Agregar a {etiqueta}", key=f"agr_{clave}"):
                        st.session_state[estado_key] = pd.concat(
                            [st.session_state[estado_key], df], ignore_index=True
                        )
                        st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")


# =========================================================
# APP
# =========================================================
init_state()

st.sidebar.title("🍧 Heladería Açaí")
st.sidebar.caption("Sistema financiero · Cobija, Bolivia")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Navegación", [
    "📊 Dashboard",
    "🛒 Ventas",
    "📦 Productos",
    "💰 Costos",
    "📈 Predicción",
    "⚖️ Punto de Equilibrio",
    "📝 Encuestas",
])

st.sidebar.markdown("---")
if st.sidebar.button("💾 Guardar todo en disco", use_container_width=True):
    persistir_todo()
    st.sidebar.success("¡Datos guardados en ./data/!")

st.sidebar.caption("v1.0 · Datos en memoria + CSV local")


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------
if menu == "📊 Dashboard":
    st.title("📊 Dashboard Ejecutivo")

    df_enr = enriquecer_ventas(st.session_state.df_ventas, st.session_state.df_productos)
    res = resumen_ventas(df_enr)
    cf = costos_fijos_totales(st.session_state.df_costos_fijos)
    cvu = costo_variable_unitario(st.session_state.df_bom)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🛒 Unidades vendidas", f"{res['unidades']:,}")
    c2.metric("💵 Ingresos", f"Bs {res['ingresos']:,.2f}")
    c3.metric("💸 Costos variables", f"Bs {res['costos']:,.2f}")
    c4.metric("📈 Utilidad bruta", f"Bs {res['utilidad']:,.2f}",
              f"{res['margen']*100:.1f}%")

    st.markdown("---")
    df_pred = predecir_ventas(st.session_state.df_prediccion)
    precio_prom = float(df_pred["precio_prom"].iloc[-1]) if not df_pred.empty else 0
    pe = punto_equilibrio(precio_prom, cvu, cf)

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("🏠 Costos fijos/mes", f"Bs {cf:,.2f}")
    c6.metric("📦 Costo variable unit.", f"Bs {cvu:,.2f}")
    c7.metric("⚖️ PE (unidades)", f"{pe['pe_unidades']:.0f} copas")
    c8.metric("💰 PE (Bs)", f"Bs {pe['pe_ingresos']:,.0f}")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🏆 Top productos por ingreso")
        top = ranking_productos(df_enr, st.session_state.df_productos)
        if not top.empty:
            fig = px.bar(top, x="ingresos", y="producto", orientation="h",
                         color="utilidad", text="unidades",
                         color_continuous_scale="Teal")
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Registra ventas para ver el ranking.")

    with col_b:
        st.subheader("📈 Proyección de ingresos")
        if not df_pred.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_pred["mes"], y=df_pred["ingresos"],
                                     mode="lines+markers", name="Ingresos",
                                     line=dict(color="#00b4d8", width=3)))
            fig.update_layout(height=350, yaxis_title="Bs")
            st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# VENTAS
# ---------------------------------------------------------
elif menu == "🛒 Ventas":
    st.title("🛒 Registro de Ventas")

    with st.form("nueva_venta", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        fecha = col1.date_input("Fecha", value=date.today())
        producto = col2.selectbox("Producto",
                                  st.session_state.df_productos["producto"].tolist())
        cantidad = col3.number_input("Cantidad", min_value=1, value=1, step=1)
        if st.form_submit_button("➕ Agregar venta", use_container_width=True):
            n = len(st.session_state.df_ventas) + 1
            nuevo = pd.DataFrame([{
                "n_trans": n, "fecha": str(fecha),
                "producto": producto, "cantidad": int(cantidad)
            }])
            st.session_state.df_ventas = pd.concat(
                [st.session_state.df_ventas, nuevo], ignore_index=True
            )
            st.success(f"Venta #{n} agregada.")
            st.rerun()

    render_importador("ventas", "Ventas", "df_ventas", modo="agregar")

    st.markdown("---")
    st.subheader("📋 Registro completo")
    df_enr = enriquecer_ventas(st.session_state.df_ventas, st.session_state.df_productos)
    if not df_enr.empty:
        st.dataframe(df_enr, use_container_width=True, hide_index=True)
        res = resumen_ventas(df_enr)
        st.info(f"**Totales:** {res['unidades']} unid · Bs {res['ingresos']:,.2f} "
                f"ingresos · Bs {res['utilidad']:,.2f} utilidad · {res['margen']*100:.1f}% margen")
        if st.button("🗑️ Borrar todas las ventas"):
            st.session_state.df_ventas = st.session_state.df_ventas.iloc[0:0]
            st.rerun()
    else:
        st.info("Aún no hay ventas registradas.")


# ---------------------------------------------------------
# PRODUCTOS
# ---------------------------------------------------------
elif menu == "📦 Productos":
    st.title("📦 Catálogo de Productos")
    st.dataframe(st.session_state.df_productos, use_container_width=True, hide_index=True)

    with st.form("nuevo_producto", clear_on_submit=True):
        c1, c2, c3, c4, c5 = st.columns(5)
        codigo = c1.text_input("Código")
        nombre = c2.text_input("Producto")
        cat = c3.text_input("Categoría")
        precio = c4.number_input("Precio (Bs)", min_value=0.0, step=0.5)
        costo = c5.number_input("Costo (Bs)", min_value=0.0, step=0.5)
        if st.form_submit_button("➕ Agregar"):
            if nombre:
                nuevo = pd.DataFrame([{
                    "codigo": codigo, "producto": nombre, "categoria": cat,
                    "precio": precio, "costo": costo
                }])
                st.session_state.df_productos = pd.concat(
                    [st.session_state.df_productos, nuevo], ignore_index=True
                )
                st.rerun()
            else:
                st.error("El nombre es obligatorio.")

    render_importador("productos", "Productos", "df_productos", modo="reemplazar")


# ---------------------------------------------------------
# COSTOS
# ---------------------------------------------------------
elif menu == "💰 Costos":
    st.title("💰 Estructura de Costos")
    tab1, tab2 = st.tabs(["🏠 Costos Fijos", "🧾 BOM (costo directo)"])

    with tab1:
        st.subheader("Costos fijos mensuales")
        st.dataframe(st.session_state.df_costos_fijos, use_container_width=True, hide_index=True)
        st.metric("Total costos fijos",
                  f"Bs {costos_fijos_totales(st.session_state.df_costos_fijos):,.2f}")

        with st.form("nuevo_cf", clear_on_submit=True):
            c1, c2, c3 = st.columns([2, 3, 1])
            cat = c1.text_input("Categoría")
            desc = c2.text_input("Descripción")
            monto = c3.number_input("Monto (Bs)", min_value=0.0, step=50.0)
            if st.form_submit_button("➕ Agregar costo fijo"):
                nuevo = pd.DataFrame([{"categoria": cat, "descripcion": desc, "monto": monto}])
                st.session_state.df_costos_fijos = pd.concat(
                    [st.session_state.df_costos_fijos, nuevo], ignore_index=True
                )
                st.rerun()

        render_importador("costos_fijos", "Costos Fijos", "df_costos_fijos", modo="reemplazar")

    with tab2:
        st.subheader("BOM – Açaí Mediano 300ml")
        st.dataframe(st.session_state.df_bom, use_container_width=True, hide_index=True)
        st.metric("Costo directo unitario",
                  f"Bs {costo_variable_unitario(st.session_state.df_bom):,.2f}")

        with st.form("nuevo_bom", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns([2, 3, 2, 1])
            comp = c1.text_input("Componente")
            det = c2.text_input("Detalle")
            cant = c3.text_input("Cantidad / unidad")
            costo = c4.number_input("Costo (Bs)", min_value=0.0, step=0.5)
            if st.form_submit_button("➕ Agregar componente"):
                nuevo = pd.DataFrame([{
                    "componente": comp, "detalle": det,
                    "cantidad": cant, "costo": costo
                }])
                st.session_state.df_bom = pd.concat(
                    [st.session_state.df_bom, nuevo], ignore_index=True
                )
                st.rerun()

        render_importador("bom", "BOM", "df_bom", modo="reemplazar")


# ---------------------------------------------------------
# PREDICCIÓN
# ---------------------------------------------------------
elif menu == "📈 Predicción":
    st.title("📈 Predicción y Proyección de Ventas")
    st.caption("Ajuste lineal sobre meses históricos, aplicado a las proyecciones")

    df_pred = predecir_ventas(st.session_state.df_prediccion)
    st.dataframe(df_pred, use_container_width=True, hide_index=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_pred["mes"], y=df_pred["unidades_ajustadas"],
                         name="Unidades", marker_color="#0077b6"))
    fig.add_trace(go.Scatter(x=df_pred["mes"], y=df_pred["ingresos"],
                             name="Ingresos (Bs)", yaxis="y2",
                             line=dict(color="#f72585", width=3)))
    fig.update_layout(
        height=450, yaxis=dict(title="Unidades"),
        yaxis2=dict(title="Bs", overlaying="y", side="right"),
        legend=dict(orientation="h"),
    )
    st.plotly_chart(fig, use_container_width=True)

    render_importador("prediccion", "Predicción", "df_prediccion", modo="reemplazar")


# ---------------------------------------------------------
# PUNTO DE EQUILIBRIO
# ---------------------------------------------------------
elif menu == "⚖️ Punto de Equilibrio":
    st.title("⚖️ Estado de Resultados y Punto de Equilibrio")

    df_pred = predecir_ventas(st.session_state.df_prediccion)
    cf = costos_fijos_totales(st.session_state.df_costos_fijos)
    cvu = costo_variable_unitario(st.session_state.df_bom)

    if df_pred.empty:
        st.warning("Necesitas datos de predicción.")
    else:
        mes_sel = st.selectbox("Mes de análisis", df_pred["mes"].tolist(),
                               index=len(df_pred) - 1)
        fila = df_pred[df_pred["mes"] == mes_sel].iloc[0]
        precio_prom = float(fila["precio_prom"])
        unidades = int(fila["unidades_ajustadas"])
        ingresos = float(fila["ingresos"])

        er = estado_resultados(ingresos, unidades, cvu, cf)
        pe = punto_equilibrio(precio_prom, cvu, cf)

        st.subheader(f"Estado de Resultados – {mes_sel}")
        df_er = pd.DataFrame([
            {"Concepto": "Ingresos totales", "Monto (Bs)": er["ingresos"]},
            {"Concepto": "(-) Costos variables", "Monto (Bs)": -er["costos_variables"]},
            {"Concepto": "(=) Margen de contribución", "Monto (Bs)": er["margen_contribucion"]},
            {"Concepto": "(-) Costos fijos", "Monto (Bs)": -er["costos_fijos"]},
            {"Concepto": "(=) EBITDA", "Monto (Bs)": er["ebitda"]},
        ])
        st.dataframe(df_er.style.format({"Monto (Bs)": "Bs {:,.2f}"}),
                     use_container_width=True, hide_index=True)

        if er["ebitda"] < 0:
            st.error(f"🚨 EBITDA negativo: Bs {er['ebitda']:,.2f}. El negocio no cubre costos en este mes.")
        else:
            st.success(f"✅ EBITDA positivo: Bs {er['ebitda']:,.2f}")

        st.subheader("⚖️ Punto de Equilibrio")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Precio prom. copa", f"Bs {precio_prom:.2f}")
        c2.metric("Costo variable unit.", f"Bs {cvu:.2f}")
        c3.metric("Margen unitario", f"Bs {pe['margen_unit']:.2f}")
        c4.metric("Costos fijos", f"Bs {cf:,.0f}")

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("PE unidades", f"{pe['pe_unidades']:.0f} copas")
        c6.metric("PE ingresos", f"Bs {pe['pe_ingresos']:,.0f}")
        c7.metric("Ventas proyectadas", f"{unidades} copas")
        margen_seg = (unidades - pe["pe_unidades"]) / unidades * 100 if unidades > 0 else -100
        c8.metric("Margen de seguridad", f"{margen_seg:.1f}%")

        if unidades < pe["pe_unidades"]:
            st.warning(
                f"⚠️ Las ventas proyectadas ({unidades}) están **por debajo** "
                f"del punto de equilibrio ({pe['pe_unidades']:.0f}). "
                f"Necesitas vender **{pe['pe_unidades']-unidades:.0f} copas más** al mes."
            )
        else:
            st.success("✅ El negocio supera el punto de equilibrio.")


# ---------------------------------------------------------
# ENCUESTAS
# ---------------------------------------------------------
elif menu == "📝 Encuestas":
    st.title("📝 Encuestas a Clientes")
    st.caption("Resultados consolidados · 100 respuestas por pregunta")

    df_enc = st.session_state.df_encuestas
    if df_enc.empty:
        st.info("No hay encuestas. Importa un CSV o agrega manualmente.")
    else:
        preguntas = df_enc["pregunta"].unique().tolist()
        for p in preguntas:
            with st.expander(f"**{p}**", expanded=False):
                sub = df_enc[df_enc["pregunta"] == p].copy()
                total = sub["respuestas"].sum()
                sub["porcentaje"] = sub["respuestas"] / total if total > 0 else 0
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.dataframe(
                        sub[["opcion", "respuestas", "porcentaje"]].style.format(
                            {"porcentaje": "{:.1%}"}
                        ),
                        use_container_width=True, hide_index=True,
                    )
                with c2:
                    fig = px.bar(sub, x="respuestas", y="opcion", orientation="h",
                                 text="respuestas", color="respuestas",
                                 color_continuous_scale="Blues")
                    fig.update_layout(height=250, showlegend=False,
                                      margin=dict(l=0, r=0, t=10, b=0))
                    st.plotly_chart(fig, use_container_width=True)

        # Formulario manual
        with st.form("nueva_encuesta", clear_on_submit=True):
            st.write("**Agregar respuesta manualmente**")
            c1, c2, c3 = st.columns([3, 2, 1])
            preg = c1.text_input("Pregunta")
            opcion = c2.text_input("Opción de respuesta")
            cant = c3.number_input("Respuestas", min_value=0, value=1, step=1)
            if st.form_submit_button("➕ Agregar"):
                nuevo = pd.DataFrame([{
                    "pregunta": preg, "opcion": opcion, "respuestas": int(cant)
                }])
                st.session_state.df_encuestas = pd.concat(
                    [st.session_state.df_encuestas, nuevo], ignore_index=True
                )
                st.rerun()

    render_importador("encuestas", "Encuestas", "df_encuestas", modo="reemplazar")