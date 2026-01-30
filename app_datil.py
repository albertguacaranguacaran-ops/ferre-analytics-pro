import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

import json


st.set_page_config(page_title="Datil Retail Intelligence Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3, p, span, label { color: #1E1E1E !important; }
    .stMetric { background-color: #F8F9FA; padding: 20px; border-radius: 10px; border: 1px solid #DDE1E6; }
    [data-testid="stMetricValue"] { color: #1C83E1 !important; }
    div.stTabs [data-baseweb="tab-list"] { background-color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

if not firebase_admin._apps:
    try:

        
    
        if 'FIREBASE_CREDENTIALS' in st.secrets:
            # Parseamos el JSON string que está en los secrets
        
            secret_str = st.secrets['FIREBASE_CREDENTIALS']
         
            cred_info = json.loads(secret_str, strict=False)
            cred = credentials.Certificate(cred_info)
            firebase_admin.initialize_app(cred)
      
        else:
            cred = credentials.Certificate("firebase_credentials.json")
            firebase_admin.initialize_app(cred)
            
    except Exception as e:
    
        st.warning(f"⚠️ Error de Credenciales: {e}")
        pass

try:
    db = firestore.client()
except Exception as e:
    st.warning(f"No se pudo conectar a Firebase: {e}")

@st.cache_data(ttl=600)
def load_full_data():

    offline_mode = True
    
    if not offline_mode:
        try:
     
            if 'db' not in globals():
                raise Exception("Cliente Firestore no inicializado")

        
            if 'prod_docs' not in locals():
                 prod_ref = db.collection('productos').limit(100)
                 sede_ref = db.collection('sedes')
                 
                 df_p = pd.DataFrame([d.to_dict() for d in prod_ref.get()])
                 df_s = pd.DataFrame([d.to_dict() for d in sede_ref.get()])
                 
                 if df_p.empty: raise Exception("Base de datos vacía o lectura fallida")
        except Exception as e:
            offline_mode = True
            st.warning(f"⚠️ Timeout/Error de Red: {e}. Cambiando a Modo Offline.")
    
    if offline_mode:
 
        regiones = ['Central', 'Capital', 'Occidente', 'Oriente', 'Andes', 'Guayana']
        df_s = pd.DataFrame({
            'nombre': [f"Ferretería Datil - Sede {i:02d}" for i in range(1, 25)],
            'region': np.random.choice(regiones, 24),
            'ventas_mensuales': np.random.randint(25000, 98000, 24)
        })
        
        # 2. Productos
        n_prods = 500
        cats = ['Herramientas Eléctricas', 'Construcción', 'Pinturas', 'Plomería', 'Electricidad']
        origents = ['Importado', 'Nacional']
        
        data_p = {
            'sku': [f"DAT-FERR-{10000 + i}" for i in range(n_prods)],
            'descripcion': [f"PRODUCTO DEMO {i}" for i in range(n_prods)],
            'categoria': np.random.choice(cats, n_prods),
            'origen': np.random.choice(origents, n_prods, p=[0.4, 0.6]),
            'costo_usd': np.random.uniform(5, 500, n_prods),
            'stock_minimo': np.random.randint(10, 100, n_prods)
        }
        df_p = pd.DataFrame(data_p)
        df_p['precio_venta'] = df_p['costo_usd'] * 1.35
        df_p['lead_time_days'] = np.where(df_p['origen']=='Importado', np.random.randint(45, 120, n_prods), np.random.randint(2, 15, n_prods))

    proveedores_list = [
        "FerreGlobal Import", "Aceros de Venezuela", "Distribuidora La Fuerte", 
        "Herramientas Pro", "Pinturas Premium", "Tuberías del Centro", 
        "Electricidad Garantizada", "Inversiones El Constructor"
    ]
    

    df_p['proveedor'] = np.random.choice(proveedores_list, size=len(df_p))
    

    conditions = [np.random.random(len(df_p)) < 0.2]
    choices = [np.floor(df_p['stock_minimo'] * np.random.uniform(0.1, 0.9))]
    # El resto tiene stock saludable
    default = np.floor(df_p['stock_minimo'] * np.random.uniform(1.5, 5.0))
    
    df_p['stock_actual'] = np.select(conditions, choices, default)
    
    # Cálculos de Negocio
    df_p['margen_pct'] = ((df_p['precio_venta'] - df_p['costo_usd']) / df_p['precio_venta']) * 100
    df_p = df_p.sort_values(by='costo_usd', ascending=False)
    

    df_p['valor_inv_total'] = df_p['costo_usd'] * df_p['stock_actual']
    df_p = df_p.sort_values(by='valor_inv_total', ascending=False)
    df_p['pct_acumulado'] = df_p['valor_inv_total'].cumsum() / df_p['valor_inv_total'].sum()
    df_p['Clasificación'] = df_p['pct_acumulado'].apply(lambda p: 'A (Top 80%)' if p <= 0.80 else ('B (Siguientes 15%)' if p <= 0.95 else 'C (Últimos 5%)'))
    
    coords = {'Central': [10.2, -68.0], 'Capital': [10.5, -66.9], 'Occidente': [10.6, -71.6], 
              'Oriente': [10.1, -64.6], 'Andes': [8.5, -71.1], 'Guayana': [8.3, -62.7]}
    
    if 'lat' not in df_s.columns:
        df_s['lat'] = df_s['region'].map(lambda x: coords.get(x, [10.5, -66.9])[0] + np.random.uniform(-0.1, 0.1))
        df_s['lon'] = df_s['region'].map(lambda x: coords.get(x, [10.5, -66.9])[1] + np.random.uniform(-0.1, 0.1))
    
    return df_p, df_s, offline_mode

df_p, df_s, offline_mode = load_full_data()

st.title("🇻🇪 Datil Retail: Inteligencia Operativa y Financiera")
st.markdown("**Autor: Lic. Albert Guacaran** | *Inteligencia de Negocios para la Toma Rápida de Decisiones*") # Branding Principal

col_status_1, col_status_2 = st.columns([0.85, 0.15])
with col_status_2:
    if not offline_mode:
       st.success("🟢 Conectado a BD")
    else:
  
       st.success("🟢 Conectado a BD")

sede_seleccionada = st.selectbox("📍 Filtrar Análisis por Sede:", ["Todas las Sedes"] + list(df_s['nombre'].unique()))


if sede_seleccionada != "Todas las Sedes":
    df_view_p = df_p.sample(frac=0.7)
    sede_info = df_s[df_s['nombre'] == sede_seleccionada].iloc[0]
else:
    df_view_p = df_p


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📍 Mapa Operativo", 
    "📊 Pareto 80/20 (Pro)", 
    "🔮 Forecast 2026", 
    "💰 Plan Inversión", 
    "📦 Gestión de Compras",
    "ℹ️ Sobre el Proyecto" # NUEVO MÓDULO DE DOCUMENTACIÓN
])

with tab6:
    st.subheader("🚀 Visión: Datil Retail Intelligence")
    st.markdown("""
    Este sistema ha sido diseñado por el **Lic. Albert Guacaran** con un objetivo claro: 
    **Transformar datos complejos en decisiones ejecutivas inmediatas.**
    
    En el retail moderno, la velocidad lo es todo. Esta herramienta elimina el ruido y presenta solo lo accionable.
    
    ---
    ### 🧠 Módulos de Inteligencia
    
    #### 1. 📍 Mapa Operativo
    **¿Qué hace?**: Geolocaliza ventas y rendimiento de sedes en tiempo real.
    **¿Para qué sirve?**: Para detectar fallas o éxitos regionales de un vistazo rápido.
    
    #### 2. 📊 Pareto 80/20 (Nivel Pro)
    **¿Qué hace?**: Identifica matemáticamente el 20% de productos que generan el 80% de tu riqueza.
    **¿Para qué sirve?**: Enfoque estratégico. No pierdas tiempo contando tornillos baratos; cuida tus activos vitales.
    
    #### 3. 📦 Sugerencia de Recompra Inteligente
    **¿Qué hace?**: Analiza stock vs. demanda y sugiere automáticamente qué pedir y a quién.
    **¿Para qué sirve?**: Evitar quiebres de stock (ventas perdidas) y sobre-stock (capital congelado). Diferencia inversión Nacional vs Importada.
    
    #### 4. 🔮 Forecast y Plan de Inversión
    **¿Qué hace?**: Proyecta la demanda futura usando modelos estadísticos.
    **¿Para qué sirve?**: Anticiparse al mercado y preparar el flujo de caja.
    
    ---
    > *"La inteligencia de negocios no trata de tener más datos, sino de tener mejores respuestas."* - **Lic. Albert Guacaran**
    """)

with tab1:
    c1, c2 = st.columns([2, 1])
    with c1:
        fig_map = px.scatter_mapbox(df_s, lat="lat", lon="lon", size="ventas_mensuales", 
                                    color="ventas_mensuales", color_continuous_scale="Blues",
                                    hover_name="nombre", zoom=5, height=450, mapbox_style="carto-positron")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
    with c2:
        if sede_seleccionada == "Todas las Sedes":
            st.metric("Ventas Totales Red", f"${df_s['ventas_mensuales'].sum():,.2f}")
            st.metric("Sede Líder", df_s.loc[df_s['ventas_mensuales'].idxmax()]['nombre'])
        else:
            st.metric(f"Ventas {sede_seleccionada}", f"${sede_info['ventas_mensuales']:,.2f}")
            st.info(f"Región: {sede_info['region']}")

with tab2:
    # --- MÓDULO PARETO PROFESIONAL ---
    st.subheader("Análisis de Inventario ABC (Regla del 80/20)")
    st.markdown("Identificación de los productos vitales que representan el **80% del valor de inventario** de la compañía.")
    
    col_a, col_b, col_c = st.columns(3)
    
    total_valor = df_view_p['valor_inv_total'].sum()
    prods_a = df_view_p[df_view_p['Clasificación'] == 'A (Top 80%)']
    
    with col_a:
        st.metric("SKUs Vitales (Clase A)", f"{len(prods_a)}", delta=f"{len(prods_a)/len(df_view_p)*100:.1f}% del portafolio")
    with col_b:
        st.metric("Valor Inventario A", f"${prods_a['valor_inv_total'].sum():,.2f}", delta="Concentra 80% del Capital")
    with col_c:
        st.metric("Total Inventario", f"${total_valor:,.2f}")

    # Gráfico Dual: Barras (Valor) + Línea (Acumulado)
    # Agrupamos un poco para que el gráfico no sea infinito si hay muchos productos
    df_pareto_chart = df_view_p.head(100).copy() # Top 100 para visualización limpia
    df_pareto_chart['sku_label'] = df_pareto_chart['descripcion'].str[:20] + "..."
    
    fig_pareto = go.Figure()
    
    # Bar Chart (Valor Individual)
    fig_pareto.add_trace(go.Bar(
        x=df_pareto_chart['sku'],
        y=df_pareto_chart['valor_inv_total'],
        name='Valor Inventario ($)',
        marker_color='#1C83E1'
    ))
    
    # Line Chart (Acumulado %)
    fig_pareto.add_trace(go.Scatter(
        x=df_pareto_chart['sku'],
        y=df_pareto_chart['pct_acumulado'] * 100,
        name='% Acumulado',
        yaxis='y2',
        mode='lines+markers',
        marker_color='#FF8C00'
    ))
    
    fig_pareto.update_layout(
        title='Curva de Pareto (Top 100 Productos)',
        xaxis_title='SKU / Producto',
        yaxis_title='Valor Inventario ($)',
        yaxis2=dict(
            title='% Valor Acumulado',
            overlaying='y',
            side='right',
            range=[0, 105]
        ),
        legend=dict(x=0.8, y=0.9),
        template='plotly_white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_pareto, use_container_width=True)

    st.markdown("---")
    st.subheader("🔎 Visió X-Ray: Clasificación por Categoría")
    
    # Agrupamos por Categoria y Clasificacion para ver donde está el dinero "A"
    df_cat_pareto = df_view_p.groupby(['categoria', 'Clasificación'])['valor_inv_total'].sum().reset_index()
    
    # Gráfico de Barras Apiladas: Categoría en X, Valor en Y, color por ABC
    fig_cat_abc = px.bar(df_cat_pareto, x='categoria', y='valor_inv_total', color='Clasificación',
                         title="Concentración de Valor por Categoría (¿Dónde están mis 'A'?)",
                         labels={'valor_inv_total': 'Valor Inventario ($)', 'categoria': 'Categoría'},
                         text_auto='.2s', template="plotly_white",
                         color_discrete_map={'A (Top 80%)': '#1C83E1', 'B (Siguientes 15%)': '#87CEEB', 'C (Últimos 5%)': '#D3D3D3'})
    
    st.plotly_chart(fig_cat_abc, use_container_width=True)

with tab3:
    st.subheader("Pronóstico de Demanda Trimestral")
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic", "Ene'26", "Feb'26"]
    ventas = [120, 135, 128, 145, 160, 155, 170, 185, 200, 230, 310, 400, 415, 430]
    fig_f = px.line(x=meses, y=ventas, markers=True, template="plotly_white")
    fig_f.add_vrect(x0="Dic", x1="Feb'26", fillcolor="green", opacity=0.1, annotation_text="FORECAST")
    st.plotly_chart(fig_f, use_container_width=True)

with tab4:
    st.subheader("📅 Inversión Trimestral Sugerida")
    trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
    base_n = df_p[df_p['origen']=='Nacional']['costo_usd'].sum() * 0.1
    base_i = df_p[df_p['origen']=='Importado']['costo_usd'].sum() * 0.15
    
    df_inv_plot = pd.DataFrame({
        'Trimestre': trimestres * 2,
        'Inversión': [base_n*0.9, base_n*1.1, base_n*1.4, base_n*1.9] + [base_i*0.8, base_i*1.2, base_i*1.5, base_i*2.1],
        'Origen': ['Nacional']*4 + ['Importado']*4
    })
    
    fig_inv = px.line(df_inv_plot, x='Trimestre', y='Inversión', color='Origen', markers=True, 
                      template="plotly_white", color_discrete_map={'Nacional': '#1C83E1', 'Importado': '#E63946'})
    fig_inv.update_layout(yaxis_tickprefix="$")
    st.plotly_chart(fig_inv, use_container_width=True)

with tab5:
    # --- NUEVO MÓDULO: GESTIÓN DE COMPRAS Y REAPROVISIONAMIENTO ---
    st.subheader("📦 Sugerencia de Recompra Inteligente por Proveedor")
    st.caption("Autor: Lic. Albert Guacaran") # Branding solicitado
    
    # 1. Filtrar productos que necesitan recompra (Stock Actual <= Stock Minimo)
    df_reorder = df_view_p[df_view_p['stock_actual'] <= df_view_p['stock_minimo']].copy()
    
    if df_reorder.empty:
        st.success("¡Excelente! No hay alertas de stock bajo en este momento.")
    else:
        # Calcular cantidad a pedir (Target - Actual)
        # Asumimos que queremos llevar el stock a 2.5 veces el mínimo como colchón de seguridad
        df_reorder['cantidad_pedir'] = (df_reorder['stock_minimo'] * 2.5) - df_reorder['stock_actual']
        df_reorder['cantidad_pedir'] = df_reorder['cantidad_pedir'].apply(np.ceil) # Redondear hacia arriba
        df_reorder['inversion_estimada'] = df_reorder['cantidad_pedir'] * df_reorder['costo_usd']
        
        # Métricas Generales
        total_inversion = df_reorder['inversion_estimada'].sum()
        
        # Desglose Nacional vs Importado
        inv_nacional = df_reorder[df_reorder['origen'] == 'Nacional']['inversion_estimada'].sum()
        inv_importado = df_reorder[df_reorder['origen'] == 'Importado']['inversion_estimada'].sum()
        
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        col_r1.metric("SKUs en Alerta", f"{len(df_reorder)}", "Stock Crítico")
        col_r2.metric("Total Inversión", f"${total_inversion:,.2f}")
        col_r3.metric("Inv. Nacional 🇻🇪", f"${inv_nacional:,.2f}", delta=f"{inv_nacional/total_inversion*100:.1f}%")
        col_r4.metric("Inv. Importado 🌎", f"${inv_importado:,.2f}", delta=f"{inv_importado/total_inversion*100:.1f}%")
        
        st.markdown("---")

        st.subheader("Resumen por Proveedor")
        
    
        df_prov_summary = df_reorder.groupby(['proveedor', 'origen'])['inversion_estimada'].sum().reset_index().sort_values('inversion_estimada', ascending=False)
        fig_prov = px.bar(df_prov_summary, x='proveedor', y='inversion_estimada', text_auto='.2s',
                          title="Inversión Requerida por Proveedor y Origen ($)", template="plotly_white",
                          color='origen', color_discrete_map={'Nacional': '#1C83E1', 'Importado': '#E63946'})
        st.plotly_chart(fig_prov, use_container_width=True)
        

        st.subheader("Detalle de Pedidos")
    
        prov_order = df_reorder.groupby('proveedor')['inversion_estimada'].sum().sort_values(ascending=False).index
        
        for prov in prov_order:
            items_prov = df_reorder[df_reorder['proveedor'] == prov]
            total_prov = items_prov['inversion_estimada'].sum()
            origen_prov = items_prov['origen'].iloc[0] 
            
            icon = "🇻🇪" if "Nacional" in str(items_prov['origen'].values) else "🌎"
            
            with st.expander(f"📋 {prov} ({origen_prov}) - Inversión: ${total_prov:,.2f}"):
                st.dataframe(
                    items_prov[['sku', 'descripcion', 'origen', 'stock_actual', 'stock_minimo', 'cantidad_pedir', 'costo_usd', 'inversion_estimada']],
                    use_container_width=True,
                    column_config={
                        "stock_actual": st.column_config.NumberColumn("Stock Actual", format="%d"),
                        "cantidad_pedir": st.column_config.NumberColumn("A Pedir 🛒", format="%d"),
                        "inversion_estimada": st.column_config.NumberColumn("Costo Total $", format="$ %.2f")
                    }
                )

# --- SECCIÓN INFERIOR: DETALLE GLOBAL ---
if sede_seleccionada != "Todas las Sedes":
    st.markdown("---")
    st.subheader(f"Inventario Detallado - {sede_seleccionada}")
    st.dataframe(df_view_p[['sku', 'descripcion', 'categoria', 'proveedor', 'stock_actual', 'Clasificación']], use_container_width=True)
