import streamlit as st

st.set_page_config(
    page_title="Calculadora de Fletes JMC-IMPORT", page_icon="📦"
)

st.title("📦 Calculadora de Fletes")
st.write(
    "Ingresa el flete total, agrega todos los productos a la lista y presiona el botón para calcular."
)

# 1. Ingreso del Flete Total
st.subheader("1. Flete General")
flete_total = st.number_input(
    "Monto total del Flete (F en S/):", min_value=0.0, value=93.0, step=1.0
)

# Inicializamos la memoria de la app
if "productos" not in st.session_state:
    st.session_state.productos = []
if "mostrar_resultados" not in st.session_state:
    st.session_state.mostrar_resultados = False

# 2. Formulario para agregar productos a la lista
st.subheader("2. Agregar Productos")
with st.form("form_producto", clear_on_submit=True):
    nombre = st.text_input("Nombre del producto (Ej: Balanza Bluetooth)")
    cantidad = st.number_input(
        "Cantidad de este producto (C.A)", min_value=1, value=1
    )
    costo_lote = st.number_input(
        "Costo Total de este Lote (C.T en S/)",
        min_value=0.0,
        value=12.0,
        step=1.0,
    )

    btn_agregar = st.form_submit_button("➕ Agregar Producto a la Lista")

    if btn_agregar and nombre:
        st.session_state.productos.append(
            {"nombre": nombre, "cantidad": cantidad, "costo_lote": costo_lote}
        )
        # Ocultamos los resultados viejos para esperar a que termine de agregar todo
        st.session_state.mostrar_resultados = False
        st.success(f"¡{nombre} agregado a la lista!")

# 3. Vista previa de la lista cargada
if st.session_state.productos:
    st.subheader("3. Lista de Productos Agregados")
    for i, p in enumerate(st.session_state.productos, 1):
        st.write(
            f"**{i}. {p['nombre'].upper()}** — {p['cantidad']} unid. — Costo lote: S/ {p['costo_lote']:.2f}"
        )

    st.divider()

    # Botón principal para procesar los cálculos
    if st.button("🧮 Calcular Fletes de Todos los Productos", type="primary"):
        st.session_state.mostrar_resultados = True

# 4. Cálculo final (Solo se ejecuta al presionar el botón)
if st.session_state.mostrar_resultados and st.session_state.productos:
    st.subheader("📊 Resultados Finales")

    # El sistema calcula el P.T sumando todos los lotes ingresados
    pt_total_pedido = sum(p["costo_lote"] for p in st.session_state.productos)

    for p in st.session_state.productos:
        # P.U = Costo del lote / Cantidad
        pu_base = p["costo_lote"] / p["cantidad"] if p["cantidad"] > 0 else 0

        # Porcentaje del lote respecto al P.T completo
        porcentaje_lote = (
            p["costo_lote"] / pt_total_pedido if pt_total_pedido > 0 else 0
        )

        # Flete proporcional del producto
        flete_lote = porcentaje_lote * flete_total
        flete_unidad = flete_lote / p["cantidad"] if p["cantidad"] > 0 else 0

        # Costo Total Individual (C.T.I)
        cti_final = pu_base + flete_unidad

        st.markdown(f"### 📦 {p['nombre'].upper()}")
        st.write(f"• **Cantidad (C.A):** {p['cantidad']} unidades")
        st.write(f"• **Precio Base por unidad (P.U):** S/ {pu_base:.2f}")
        st.write(f"• **Flete por unidad:** S/ {flete_unidad:.2f}")
        st.success(
            f"➔ **COSTO FINAL UNITARIO (C.T.I): S/ {cti_final:.2f} c/u**"
        )
        st.divider()

    # Resumen general del pedido
    st.subheader("📋 Resumen del Pedido")
    st.write(f"• **Suma Total de Productos (P.T):** S/ {pt_total_pedido:.2f}")
    st.write(f"• **Flete Total (F):** S/ {flete_total:.2f}")
    st.write(
        f"• **TOTAL GENERAL A PAGAR:** S/ {(pt_total_pedido + flete_total):.2f}"
    )

    if st.button("🗑️ Limpiar Todo para Nuevo Pedido"):
        st.session_state.productos = []
        st.session_state.mostrar_resultados = False
        st.rerun()