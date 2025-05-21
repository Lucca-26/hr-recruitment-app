import streamlit as st
import pandas as pd
import numpy as np
import json
from helpers.data_loader import load_data

# Configuração da página
st.set_page_config(
    page_title="HR Match - Decision/FIAP",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e cabeçalho
st.title("💼 HR Match - Decision")
st.markdown("### Sistema inteligente de correspondência entre candidatos e vagas")

# Logo da Decision estilizado
st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <div style="text-align: center; background: linear-gradient(135deg, #005F9E 0%, #00417A 100%); color: white; padding: 15px; border-radius: 8px; width: 300px; box-shadow: 0 3px 6px rgba(0,0,0,0.16); user-select: none;">
            <h1 style="margin: 0; font-size: 36px; font-weight: 700; letter-spacing: 1px;">DECISION</h1>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Gestão de Recursos Humanos</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Dashboard principal
st.markdown("## Dashboard Principal")

# Carregamento de dados
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

# Indicadores principais
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Vagas Disponíveis", value=len(vagas_df))
with col2:
    st.metric(label="Candidatos Cadastrados", value=len(applicants_df))
with col3:
    st.metric(label="Prospectos em Processo", value=len(prospects_df))

# Exibir vagas recentes
st.markdown("### Vagas Recentes")
if 'vagas_df' in st.session_state:
    recent_vagas = vagas_df.head(5)
    
    for idx, row in recent_vagas.iterrows():
        expander = st.expander(f"{row['titulo_vaga']} - {row['cliente']}")
        with expander:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Cliente:** {row['cliente']}")
                st.markdown(f"**Local:** {row['cidade']}, {row['estado']}")
                st.markdown(f"**Nível:** {row['nivel_profissional']}")
            with col2:
                st.markdown(f"**Idiomas necessários:**")
                st.markdown(f"- Inglês: {row['nivel_ingles']}")
                st.markdown(f"- Espanhol: {row['nivel_espanhol']}")
                st.markdown(f"**Formação:** {row['nivel_academico']}")

# Informações sobre as páginas
st.markdown("## 📌 Navegue pela aplicação")
st.markdown("""
- **🔍 Matching Tool**: Encontre os candidatos mais adequados para cada vaga
- **📊 Analytics**: Visualize estatísticas e insights sobre o processo de recrutamento
- **📝 Documentation**: Consulte a documentação do sistema
""")

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido para Decision/FIAP | © 2025")

# Rodapé com nomes da equipe
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