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

# ⭐ CONFIGURAR TEMA CLARO GLOBAL
def set_light_theme():
    st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stApp {
        background-color: #ffffff;
    }
    .css-1d391kg, .css-1y4p8pa {
        background-color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #2d3748 !important;
    }
    </style>
    """, unsafe_allow_html=True)

set_light_theme()

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
                       72.5, 18.1, 8.8],
        
        'Riesgo': ['Bajo', 'Moderado', 'Alto', 'Muy Alto',
                   'Alto', 'Moderado', 'Bajo',
                   'Bajo', 'Moderado', 'Alto', 'Muy Alto',
                   'Bajo', 'Moderado', 'Alto']
    }

    df = pd.DataFrame(data)
    
    # ⭐ NUEVA PALETA DE COLORES OSCUROS PROFESIONAL
    color_scale = {
        'Bajo': '#2e7d32',      # Verde oscuro
        'Moderado': '#1565c0',  # Azul oscuro (nuevo color)
        'Alto': '#ef6c00',      # Naranja oscuro
        'Muy Alto': '#c62828'   # Rojo oscuro
    }
    
    # Metas terapéuticas
    metas = {
        'LDL': 31.9,      # Óptimo (<100)
        'HDL': 56.4,      # Intermedio + Deseable (53.2 + 3.2)
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
                marker_color=color_scale[row['Riesgo']],
                marker_line_color='white',
                marker_line_width=1.5,
                opacity=0.9,
                text=f"{row['Porcentaje']}%",
                textposition='inside',
                textfont=dict(color='white', size=10, weight='bold'),  # ⭐ Texto siempre blanco para mejor contraste
                # ⭐ ELIMINADO: hovertemplate con "Riesgo"
                hovertemplate=f"<b>{row['Categoría']}</b><br>Porcentaje: {row['Porcentaje']}%<extra></extra>"
            ))
            bottom += row['Porcentaje']

    # Líneas de meta
    for i, (variable, meta) in enumerate(metas.items()):
        fig.add_shape(
            type="line",
            x0=i-0.4, x1=i+0.4,
            y0=meta, y1=meta,
            line=dict(color="#1a237e", width=3, dash="dash"),  # ⭐ Azul más oscuro
            opacity=0.8
        )
        
        fig.add_annotation(
            x=i, y=meta + 5,
            text=f"Meta: {meta}%",
            showarrow=False,
            bgcolor="white",
            bordercolor="#1a237e",
            borderwidth=1,
            font=dict(size=10, color="#1a237e", weight='bold')
        )

    # ⭐ PERSONALIZACIÓN MEJORADA
    fig.update_layout(
        title=dict(
            text="<b>DISTRIBUCIÓN POR CATEGORÍAS DE RIESGO Y CUMPLIMIENTO DE METAS</b><br><sub>Porcentaje de pacientes en cada categoría clínica</sub>",
            x=0.5,
            font=dict(size=20, family="Arial", color="#1a237e")  # ⭐ Color oscuro
        ),
        xaxis=dict(
            title="<b>Parámetro Lipídico</b>",
            title_font=dict(size=14, color="#1a237e"),
            tickfont=dict(size=12, weight='bold', color="#1a237e")
        ),
        yaxis=dict(
            title="<b>Porcentaje de Pacientes (%)</b>",
            title_font=dict(size=14, color="#1a237e"),
            tickfont=dict(size=12, color="#1a237e"),
            range=[0, 110]
        ),
        barmode='stack',
        showlegend=True,
        # ⭐ BARRAS MÁS ANCHAS - reducido espaciado
        bargap=0.3,
        bargroupgap=0.1,
        legend=dict(
            title="<b>Categorías Clínicas</b>",
            title_font=dict(color="#1a237e"),
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.05,
            bgcolor='white',
            bordercolor='#1a237e',
            borderwidth=1,
            font=dict(color="#1a237e")
        ),
        plot_bgcolor='white',  # ⭐ Fondo blanco
        paper_bgcolor='white', # ⭐ Fondo blanco
        font=dict(family="Arial", color="#1a237e"),  # ⭐ Color oscuro global
        width=1000,
        height=600,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            font_color="#1a237e"
        )
    )

    return fig

# =============================================================================
# INTERFAZ DE STREAMLIT
# =============================================================================

# Sidebar
with st.sidebar:
    st.title("🫀 Dashboard Lipídico")
    st.markdown("---")
    st.markdown("**Análisis de distribución** de pacientes según categorías de riesgo cardiovascular")
    st.markdown("---")
    st.caption("Desarrollado para análisis clínico")
    st.caption("Datos actualizados 2024")

# Contenido principal
st.title("🎯 DASHBOARD LIPÍDICO - ANÁLISIS CLÍNICO")
st.markdown("Distribución de pacientes según categorías de riesgo basada en valores promedios intraindividuales")

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
st.plotly_chart(fig, use_container_width=True)

# Notas al pie
st.markdown("---")
st.markdown("**Notas:**")
st.markdown("- *Línea punteada:* Porcentaje que alcanzó la meta terapéutica")
st.markdown("- **Colores:** Verde oscuro (Bajo riesgo) → Azul (Moderado) → Naranja (Alto) → Rojo oscuro (Muy alto)")
st.markdown("- **Interactividad:** Haz hover sobre las barras para ver detalles")

# Footer
st.markdown("---")
st.caption("© 2024 - Dashboard desarrollado para investigación clínica")
