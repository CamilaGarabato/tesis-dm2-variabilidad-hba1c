import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA - ELEGANTE
# =============================================================================
st.set_page_config(
    page_title="Dashboard Lipídico Clínico",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TEMA ELEGANTE - fondo oscuro profesional
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
    }
    .stApp {
        background-color: #0f172a;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #f8fafc !important;
    }
    .st-bb {
        background-color: transparent;
    }
    .css-1d391kg {
        background-color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# FUNCIÓN PRINCIPAL DEL DASHBOARD
# =============================================================================
def create_interactive_lipid_dashboard():
    # Datos actualizados
    data = {
        'Variable': ['LDL', 'LDL', 'LDL', 'LDL', 
                     'HDL', 'HDL', 'HDL',
                     'Triglicéridos', 'Triglicéridos', 'Triglicéridos', 'Triglicéridos',
                     'Colesterol Total', 'Colesterol Total', 'Colesterol Total'],
        
        'Categoría': ['Óptimo (<100 mg/dL)', 'Casi óptimo (100-129 mg/dL)', 'Límite alto (130-159 mg/dL)', 'Alto+Muy alto (≥160 mg/dL)',
                      'Bajo (<40 mg/dL)', 'Intermedio (40-59 mg/dL)', 'Deseable/Alto (≥60 mg/dL)', 
                      'Normal (<150 mg/dL)', 'Levemente elevados (150-199)', 'Moderada (200-499 mg/dL)', 'Severa (≥500 mg/dL)',
                      'Deseable (<200 mg/dL)', 'Límite alto (200-239 mg/dL)', 'Alto (≥240 mg/dL)'],
        
        'Porcentaje': [31.9, 39.4, 17.0, 9.0,
                       39.4, 53.2, 3.2,
                       32.6, 27.5, 36.3, 2.6,
                       72.5, 18.1, 8.8]
    }

    df = pd.DataFrame(data)
    
    # PALETA INTELIGENTE - UN COLOR POR PARÁMETRO
    color_scale = {
        # LDL - Escala azul-púrpura sofisticada
        'Óptimo (<100 mg/dL)': '#1a237e',        # Azul índigo oscuro
        'Casi óptimo (100-129 mg/dL)': '#283593', # Azul pizarra
        'Límite alto (130-159 mg/dL)': '#303f9f',  # Azul violáceo
        'Alto+Muy alto (≥160 mg/dL)': '#3949ab',   # Azul real profundo
        
        # HDL - Escala de verdes oscuros intensos
        'Bajo (<40 mg/dL)': '#1b5e20',        # Verde muy oscuro, casi negro-verde
        'Intermedio (40-59 mg/dL)': '#2e7d32', # Verde bosque intenso
        'Deseable/Alto (≥60 mg/dL)': '#388e3c',  # Verde esmeralda fuerte
        
        # Triglicéridos - Escala de naranjas oscuros intensos
        'Normal (<150 mg/dL)': '#e65100',        # Naranja oscuro intenso
        'Levemente elevados (150-199)': '#ef6c00', # Naranja óxido
        'Moderada (200-499 mg/dL)': '#f57c00',    # Naranja calabaza
        'Severa (≥500 mg/dL)': '#ff9800',         # Naranja vibrante pero sobrio
                
        # Colesterol Total - Escala de púrpuras oscuros intensos
        'Deseable (<200 mg/dL)': '#4a148c',        # Púrpura muy oscuro
        'Límite alto (200-239 mg/dL)': '#6a1b9a',  # Púrpura uva intenso
        'Alto (≥240 mg/dL)': '#8e24aa',            # Púrpura vibrante pero sobrio
    }
    
    # Metas terapéuticas
    metas = {
        'LDL': 31.9,      # Óptimo (<100)
        'HDL': 56.4,      # Intermedio + Deseable
        'Triglicéridos': 32.6,  # Normal
        'Colesterol Total': 72.5  # Deseable
    }

    # Crear figura Plotly
    fig = go.Figure()

    # Variables en orden
    variables = ['LDL', 'HDL', 'Triglicéridos', 'Colesterol Total']
    
    # Añadir barras apiladas
    for i, variable in enumerate(variables):
        subset = df[df['Variable'] == variable]
        bottom = 0
        
        for _, row in subset.iterrows():
            fig.add_trace(go.Bar(
                name=row['Categoría'],
                x=[variable],
                y=[row['Porcentaje']],
                offsetgroup=i,
                base=bottom,
                marker_color=color_scale[row['Categoría']],
                marker_line_color='white',
                marker_line_width=1.5,
                opacity=0.95,
                text=f"{row['Porcentaje']}%",
                textposition='inside',
                textfont=dict(color='white', size=10, weight='bold'),
                hovertemplate=f"<b>{row['Categoría']}</b><br>Pacientes: {row['Porcentaje']}%<extra></extra>",
                width=0.8
            ))
            bottom += row['Porcentaje']

    # Líneas de meta
    for i, (variable, meta) in enumerate(metas.items()):
        fig.add_shape(
            type="line",
            x0=i-0.4, x1=i+0.4,
            y0=meta, y1=meta,
            line=dict(color="#ffffff", width=3, dash="dash"),
            opacity=0.9
        )
        
        fig.add_annotation(
            x=i, y=meta + 5,
            text=f"Meta: {meta}%",
            showarrow=False,
            bgcolor="rgba(0,0,0,0.8)",
            bordercolor="#ffffff",
            borderwidth=1,
            font=dict(size=11, color="#ffffff", weight='bold')
        )

    # DISEÑO ELEGANTE - gráfico blanco sobre fondo oscuro
    fig.update_layout(
        title=dict(
            text="<b>DISTRIBUCIÓN POR CATEGORÍAS CLÍNICAS</b><br><sub>Porcentaje de pacientes en cada categoría</sub>",
            x=0.5,
            font=dict(size=20, family="Consolas", color="#ffffff")
        ),
        xaxis=dict(
            title="<b>PARÁMETRO LIPÍDICO</b>",
            title_font=dict(size=16, color="#ffffff"),
            tickfont=dict(size=14, weight='bold', color="#ffffff"),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title="<b>PORCENTAJE DE PACIENTES (%)</b>",
            title_font=dict(size=16, color="#ffffff"),
            tickfont=dict(size=12, color="#ffffff"),
            range=[0, 110],
            gridcolor='rgba(255,255,255,0.1)'
        ),
        barmode='stack',
        showlegend=False,  # ⭐ ELIMINADA LA LEYENDA CONFUSA
        bargap=0.15,
        bargroupgap=0.05,
        plot_bgcolor='white',  # ⭐ GRÁFICO CON FONDO BLANCO
        paper_bgcolor='rgba(0,0,0,0)',  # ⭐ FONDO TRANSPARENTE
        font=dict(family="Arial", color="#ffffff"),
        width=1000,
        height=600,
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#000000",
            font_size=12,
            font_family="Consolas",
            font_color="#000000"
        )
    )

    return fig

# =============================================================================
# INTERFAZ DE STREAMLIT
# =============================================================================

# Sidebar 
with st.sidebar:
    st.title("🫀 DASHBOARD LIPÍDICO")
    st.markdown("---")
    st.markdown("**Análisis de distribución** de pacientes según categorías clínicas")
    st.markdown("---")
    
    # ⭐ GUÍA DE COLORES SIMPLE
    st.markdown("**GUÍA DE COLORES:**")
    st.markdown("🔵 **LDL** - Escala de azules")
    st.markdown("🟢 **HDL** - Escala de verdes/rojos")  
    st.markdown("🟠 **Triglicéridos** - Escala de naranjas")
    st.markdown("🟣 **Colesterol Total** - Escala de púrpuras")
    
    st.markdown("---")
    st.caption("Desarrollado para análisis clínico")
    st.caption("Datos actualizados 2024")

# Contenido principal
st.title("ANÁLISIS DEL PERFIL LIPÍDICO")
st.markdown("Distribución de pacientes según categorías basada en valores promedios intraindividuales")

# KPIs en columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("LDL en Meta", "31.9%", "68.1% fuera de meta")

with col2:
    st.metric("HDL en Meta", "56.4%", "43.6% fuera de meta")

with col3:
    st.metric("Triglicéridos en Meta", "32.6%", "67.4% fuera de meta")

with col4:
    st.metric("Colesterol Total en Meta", "72.5%", "27.5% fuera de meta")

st.markdown("---")

# Gráfico principal
fig = create_interactive_lipid_dashboard()
st.plotly_chart(fig, width="stretch")

# Notas al pie
st.markdown("---")
st.markdown("**NOTAS:**")
st.markdown("- *Línea punteada:* Porcentaje que alcanzó la meta terapéutica")
st.markdown("- **Colores:** Cada parámetro tiene su propia escala de colores, cuya intensidad varia según densidad de datos")
st.markdown("- **Interactividad:** Haz hover sobre las barras para ver detalles")

# Footer
st.markdown("---")
st.caption("© Estudio retrospectivo 2020 - 2025 - Dashboard desarrollado para el analisis de datos")
