import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from helpers.data_loader import load_data

# Configuração da página
st.set_page_config(
    page_title="HR Match - Analytics",
    page_icon="📊",
    layout="wide"
)

# Logo da Decision estilizado
st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <div style="text-align: center; background: linear-gradient(135deg, #005F9E 0%, #00417A 100%); color: white; padding: 15px; border-radius: 8px; width: 300px; box-shadow: 0 3px 6px rgba(0,0,0,0.16); user-select: none;">
            <h1 style="margin: 0; font-size: 36px; font-weight: 700; letter-spacing: 1px;">DECISION</h1>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Gestão de Recursos Humanos</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.title("📊 Analytics")
st.markdown("### Visualize estatísticas e insights sobre o processo de recrutamento")

# Inicializar estado da sessão para dados se ainda não estiver feito
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

# Criar abas para seções de análises
tab1, tab2, tab3 = st.tabs(["Visão Geral", "Análise de Vagas", "Análise de Candidatos"])

with tab1:
    st.markdown("### Visão Geral do Processo de Recrutamento")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Vagas",
            value=len(vagas_df)
        )
    
    with col2:
        st.metric(
            label="Total de Candidatos",
            value=len(applicants_df)
        )
    
    with col3:
        st.metric(
            label="Total de Prospectos",
            value=len(prospects_df)
        )
    
    with col4:
        # Contar prospectos únicos
        unique_prospects = prospects_df['codigo'].nunique()
        st.metric(
            label="Candidatos em Processo",
            value=unique_prospects
        )
    
    # Distribuição de status do processo
    if not prospects_df.empty:
        # Contar ocorrências de status
        status_counts = prospects_df['situacao_candidado'].value_counts().reset_index()
        status_counts.columns = ['Situação', 'Contagem']
        
        # Criar gráfico de barras horizontal
        fig = px.bar(
            status_counts,
            y='Situação',
            x='Contagem',
            orientation='h',
            title='Distribuição de Status dos Candidatos',
            labels={'Contagem': 'Número de Candidatos', 'Situação': 'Status'},
            color='Contagem',
            color_continuous_scale=px.colors.sequential.Blues
        )
        
        st.plotly_chart(fig)
    
    # Série temporal de candidaturas
    if not prospects_df.empty and 'data_candidatura' in prospects_df.columns:
        # Converter strings de data para datetime
        prospects_df['data_candidatura_dt'] = pd.to_datetime(
            prospects_df['data_candidatura'], 
            format='%d-%m-%Y', 
            errors='coerce'
        )
        
        # Agrupar por data e contar
        time_series = prospects_df.groupby(
            prospects_df['data_candidatura_dt'].dt.to_period('M')
        ).size().reset_index()
        
        time_series.columns = ['Mês', 'Candidaturas']
        time_series['Mês'] = time_series['Mês'].astype(str)
        
        # Criar gráfico de linha
        fig = px.line(
            time_series,
            x='Mês',
            y='Candidaturas',
            title='Volume de Candidaturas por Mês',
            labels={'Candidaturas': 'Número de Candidaturas', 'Mês': 'Mês'},
            markers=True
        )
        
        st.plotly_chart(fig)

with tab2:
    st.markdown("### Análise de Vagas")
    
    if not vagas_df.empty:
        # Distribuição de vagas por área
        if 'areas_atuacao' in vagas_df.columns:
            # Dividir e contar áreas
            areas = vagas_df['areas_atuacao'].str.split('-').explode().str.strip()
            area_counts = areas.value_counts().head(10).reset_index()
            area_counts.columns = ['Área', 'Contagem']
            
            # Criar gráfico de barras horizontal
            fig = px.bar(
                area_counts,
                y='Área',
                x='Contagem',
                orientation='h',
                title='Top 10 Áreas de Atuação das Vagas',
                labels={'Contagem': 'Número de Vagas', 'Área': 'Área de Atuação'},
                color='Contagem',
                color_continuous_scale=px.colors.sequential.Greens
            )
            
            st.plotly_chart(fig)
        
        # Distribuição de vagas por localização
        if 'estado' in vagas_df.columns and 'cidade' in vagas_df.columns:
            # Criar coluna de localização
            vagas_df['localização'] = vagas_df['cidade'] + ', ' + vagas_df['estado']
            
            # Contar vagas por localização
            location_counts = vagas_df['localização'].value_counts().head(10).reset_index()
            location_counts.columns = ['Localização', 'Contagem']
            
            # Criar gráfico de barras horizontal
            fig = px.bar(
                location_counts,
                y='Localização',
                x='Contagem',
                orientation='h',
                title='Top 10 Localizações das Vagas',
                labels={'Contagem': 'Número de Vagas', 'Localização': 'Localização'},
                color='Contagem',
                color_continuous_scale=px.colors.sequential.Purples
            )
            
            st.plotly_chart(fig)
        
        # Distribuição de vagas por nível acadêmico
        if 'nivel_academico' in vagas_df.columns:
            # Contar vagas por nível acadêmico
            academic_counts = vagas_df['nivel_academico'].value_counts().reset_index()
            academic_counts.columns = ['Nível Acadêmico', 'Contagem']
            
            # Criar gráfico de pizza
            fig = px.pie(
                academic_counts,
                values='Contagem',
                names='Nível Acadêmico',
                title='Distribuição de Vagas por Nível Acadêmico'
            )
            
            st.plotly_chart(fig)
        
        # Distribuição de vagas por nível de inglês
        if 'nivel_ingles' in vagas_df.columns:
            # Contar vagas por nível de inglês
            english_counts = vagas_df['nivel_ingles'].value_counts().reset_index()
            english_counts.columns = ['Nível de Inglês', 'Contagem']
            
            # Criar gráfico de pizza
            fig = px.pie(
                english_counts,
                values='Contagem',
                names='Nível de Inglês',
                title='Distribuição de Vagas por Nível de Inglês'
            )
            
            st.plotly_chart(fig)

with tab3:
    st.markdown("### Análise de Candidatos")
    
    if not applicants_df.empty:
        # Distribuição de candidatos por área
        if 'area_atuacao' in applicants_df.columns:
            # Dividir e contar áreas
            applicants_df['area_atuacao'] = applicants_df['area_atuacao'].astype(str)
            areas = applicants_df['area_atuacao'].str.split(',').explode().str.strip()
            area_counts = areas.value_counts().head(10).reset_index()
            area_counts.columns = ['Área', 'Contagem']
            
            # Criar gráfico de barras horizontal
            fig = px.bar(
                area_counts,
                y='Área',
                x='Contagem',
                orientation='h',
                title='Top 10 Áreas de Atuação dos Candidatos',
                labels={'Contagem': 'Número de Candidatos', 'Área': 'Área de Atuação'},
                color='Contagem',
                color_continuous_scale=px.colors.sequential.Reds
            )
            
            st.plotly_chart(fig)
        
        # Distribuição de candidatos por nível acadêmico
        if 'nivel_academico' in applicants_df.columns:
            # Contar candidatos por nível acadêmico
            academic_counts = applicants_df['nivel_academico'].value_counts().reset_index()
            academic_counts.columns = ['Nível Acadêmico', 'Contagem']
            
            # Criar gráfico de pizza
            fig = px.pie(
                academic_counts,
                values='Contagem',
                names='Nível Acadêmico',
                title='Distribuição de Candidatos por Nível Acadêmico'
            )
            
            st.plotly_chart(fig)
        
        # Distribuição de candidatos por nível de inglês
        if 'nivel_ingles' in applicants_df.columns:
            # Contar candidatos por nível de inglês
            english_counts = applicants_df['nivel_ingles'].value_counts().reset_index()
            english_counts.columns = ['Nível de Inglês', 'Contagem']
            
            # Criar gráfico de pizza
            fig = px.pie(
                english_counts,
                values='Contagem',
                names='Nível de Inglês',
                title='Distribuição de Candidatos por Nível de Inglês'
            )
            
            st.plotly_chart(fig)
    
    # Análise de duração do processo
    if not prospects_df.empty and 'data_candidatura' in prospects_df.columns and 'ultima_atualizacao' in prospects_df.columns:
        # Converter strings de data para datetime
        prospects_df['data_candidatura_dt'] = pd.to_datetime(
            prospects_