import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from PIL import Image
import plotly.express as px
from helpers.data_loader import load_data
from helpers.text_processor import preprocess_text
from helpers.similarity_calculator import calculate_similarity

# Set page configuration
st.set_page_config(
    page_title="HR Match - Decision",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add header
st.title("💼 HR Match - Decision")
st.markdown("### Sistema inteligente de correspondência entre candidatos e vagas")

# Em vez de usar o logo, adicionar o nome da empresa em estilo de logo
st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <div style="text-align: center; background: linear-gradient(135deg, #005F9E 0%, #00417A 100%); color: white; padding: 15px; border-radius: 8px; width: 300px; box-shadow: 0 3px 6px rgba(0,0,0,0.16); user-select: none;">
            <h1 style="margin: 0; font-size: 36px; font-weight: 700; letter-spacing: 1px;">DECISION</h1>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Gestão de Recursos Humanos</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main dashboard
st.markdown("## Dashboard Principal")

# Load data
if 'data_loaded' not in st.session_state:
    with st.spinner("Carregando dados... Por favor, aguarde."):
        try:
            vagas_df, prospects_df, applicants_df = load_data()
            st.session_state['vagas_df'] = vagas_df
            st.session_state['prospects_df'] = prospects_df
            st.session_state['applicants_df'] = applicants_df
            st.session_state['data_loaded'] = True
        except Exception as e:
            st.error(f"Erro ao carregar os dados: {e}")
else:
    vagas_df = st.session_state['vagas_df']
    prospects_df = st.session_state['prospects_df']
    applicants_df = st.session_state['applicants_df']

# Show key metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Número de Vagas Disponíveis", value=len(vagas_df))

with col2:
    st.metric(label="Candidatos Cadastrados", value=len(applicants_df))

with col3:
    st.metric(label="Prospectos em Processo", value=len(prospects_df))

# Show recent job postings
st.markdown("### Vagas Recentes")
if 'vagas_df' in st.session_state:
    # Extract a subset of recent vacancies for display
    recent_vagas = vagas_df.head(5)
    
# Debug para ver as colunas disponíveis
st.write("Colunas disponíveis:", list(recent_vagas.columns))

for idx, row in recent_vagas.iterrows():
    # Verifica se as colunas existem antes de acessá-las
    titulo = row.get('titulo_vaga', 'Título não disponível')
    cliente = row.get('cliente', 'Cliente não disponível')
    
    expander = st.expander(f"{titulo} - {cliente}")
    with expander:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Cliente:** {row.get('cliente', 'N/A')}")
            cidade = row.get('cidade', 'N/A')
            estado = row.get('estado', 'N/A')
            st.markdown(f"**Local:** {cidade}, {estado}")
            st.markdown(f"**Nível:** {row.get('nivel_profissional', 'N/A')}")
        with col2:
            st.markdown(f"**Idiomas necessários:**")
            st.markdown(f"- Inglês: {row.get('nivel_ingles', 'N/A')}")
            st.markdown(f"- Espanhol: {row.get('nivel_espanhol', 'N/A')}")
            st.markdown(f"**Formação:** {row.get('nivel_academico', 'N/A')}")

# Add information about the pages
st.markdown("## 📌 Navegue pela aplicação")
st.markdown("""
- **🔍 Matching Tool**: Encontre os candidatos mais adequados para cada vaga
- **📊 Analytics**: Visualize estatísticas e insights sobre o processo de recrutamento
- **📝 Documentation**: Consulte a documentação do sistema
""")

st.markdown("---")
st.markdown("Desenvolvido para Decision/FIAP | © 2025")

# Rodapé com nomes da equipe alinhado à direita
st.markdown(
    """
    <div style="position: fixed; bottom: 10px; right: 20px; text-align: right; font-size: 14px;">
        <b>Grupo 9 | 6DTAT:</b><br>
        Francisco das Chagas Alcântara Júnior – RM 357554<br>
        Geovana Façanha da Silva – RM357215<br>
        Luciana Conceição Ferreira – RM357220
    </div>
    """,
    unsafe_allow_html=True
)
