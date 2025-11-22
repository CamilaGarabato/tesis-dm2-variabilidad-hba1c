import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Dashboard Lipídico Clínico",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TEMA CLARO AGGRESIVO
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
    }
    .stApp {
        background-color: #FFFFFF;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #000000 !important;
    }
    .st-bb {
        background-color: transparent;
    }
    .css-1d391kg {
        background-color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# FUNCIÓN PRINCIPAL DEL DASHBOARD
# =============================================================================
def create_interactive_lipid_dashboard():
    # Datos actualizados SIN columna de riesgo
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
    
    # PALETA DE COLORES SIMPLIFICADA - sin referencia a riesgo
    color_scale = {
        'Óptimo (<100 mg/dL)': '#2e7d32',           # Verde oscuro
        'Casi óptimo (100-129 mg/dL)': '#1565c0',   # Azul
        'Límite alto (130-159 mg/dL)': '#ff8f00',   # Naranja
        'Alto+Muy alto (≥160 mg/dL)': '#c62828',    # Rojo
        
        'Bajo (<40 mg/dL)': '#c62828',              # Rojo
        'Intermedio (40-59 mg/dL)': '#1565c0',      # Azul  
        'Deseable/Alto (≥60 mg/dL)': '#2e7d32',     # Verde
        
        'Normal (<150 mg/dL)': '#2e7d32',           # Verde
        'Levemente elevados (150-199)': '#1565c0',  # Azul
        'Moderada (200-499 mg/dL)': '#ff8f00',      # Naranja
        'Severa (≥500 mg/dL)': '#c62828',           # Rojo
        
        'Deseable (<200 mg/dL)': '#2e7d32',         # Verde
        'Límite alto (200-239 mg/dL)': '#1565c0',   # Azul
        'Alto (≥240 mg/dL)': '#c62828'              # Rojo
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
    
    # Añadir barras apiladas - MUCHO MÁS ANCHAS
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
                marker_line_width=2,
                opacity=0.95,
                text=f"{row['Porcentaje']}%",
                textposition='inside',
                textfont=dict(color='white', size=11, weight='bold'),
                # TOOLTIP SIMPLE - sin mención de riesgo
                hovertemplate=f"<b>{row['Categoría']}</b><br>Pacientes: {row['Porcentaje']}%<extra></extra>",
                width=0.8  # BARRAS MUCHO MÁS ANCHAS
            ))
            bottom += row['Porcentaje']

    # Líneas de meta
    for i, (variable, meta) in enumerate(metas.items()):
        fig.add_shape(
            type="line",
            x0=i-0.4, x1=i+0.4,
            y0=meta, y1=meta,
            line=dict(color="#000000", width=3, dash="dash"),
            opacity=0.9
        )
        
        fig.add_annotation(
            x=i, y=meta + 5,
            text=f"Meta: {meta}%",
            showarrow=False,
            bgcolor="white",
            bordercolor="#000000",
            borderwidth=2,
            font=dict(size=11, color="#000000", weight='bold')
        )

    # PERSONALIZACIÓN EXTREMA - MÁXIMO CONTRASTE
    fig.update_layout(
        title=dict(
            text="<b>DISTRIBUCIÓN POR CATEGORÍAS DE RIESGO</b><br><sub>Porcentaje de pacientes en cada categoría clínica</sub>",
            x=0.5,
            font=dict(size=22, family="Arial", color="#000000")
        ),
        xaxis=dict(
            title="<b>PARÁMETRO LIPÍDICO</b>",
            title_font=dict(size=16, color="#000000"),
            tickfont=dict(size=14, weight='bold', color="#000000"),
            gridcolor='#e0e0e0'
        ),
        yaxis=dict(
            title="<b>PORCENTAJE DE PACIENTES (%)</b>",
            title_font=dict(size=16, color="#000000"),
            tickfont=dict(size=12, color="#000000"),
            range=[0, 110],
            gridcolor='#e0e0e0'
        ),
        barmode='stack',
        showlegend=True,
        # BARRAS MUY ANCHAS - mínimo espacio entre grupos
        bargap=0.15,
        bargroupgap=0.05,
        legend=dict(
            title="<b>CATEGORÍAS CLÍNICAS</b>",
            title_font=dict(size=12, color="#000000"),
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bgcolor='white',
            bordercolor='#000000',
            borderwidth=2,
            font=dict(size=10, color="#000000")
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", color="#000000"),
        width=1100,
        height=650,
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#000000",
            font_size=12,
            font_family="Arial",
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
    st.caption("Desarrollado para análisis clínico")
    st.caption("Datos actualizados 2024")

# Contenido principal
st.title(" ANÁLISIS DEL PERFIL LIPÍDICO")
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

# Gráfico principal - ⭐ LÍNEA CORREGIDA
fig = create_interactive_lipid_dashboard()
st.plotly_chart(fig, width="stretch")

# Notas al pie
st.markdown("---")
st.markdown("**NOTAS:**")
st.markdown("- *Línea punteada:* Porcentaje que alcanzó la meta terapéutica")
st.markdown("- **Interactividad:** Haz hover sobre las barras para ver detalles")

# Footer
st.markdown("---")
st.caption("© 2024 - Dashboard desarrollado para investigación clínica")
