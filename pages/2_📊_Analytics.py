import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from helpers.data_loader import load_data

# Set page configuration
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

# Initialize session state for data if not already done
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

# Create tabs for analytics sections
tab1, tab2, tab3 = st.tabs(["Visão Geral", "Análise de Vagas", "Análise de Candidatos"])

with tab1:
    st.markdown("### Visão Geral do Processo de Recrutamento")
    
    # Key metrics
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
        # Count unique prospects
        unique_prospects = prospects_df['codigo'].nunique()
        st.metric(
            label="Candidatos em Processo",
            value=unique_prospects
        )
    
    # Process status distribution
    if not prospects_df.empty:
        # Count status occurrences
        status_counts = prospects_df['situacao_candidado'].value_counts().reset_index()
        status_counts.columns = ['Situação', 'Contagem']
        
        # Create horizontal bar chart
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
    
    # Time series of applications
    if not prospects_df.empty and 'data_candidatura' in prospects_df.columns:
        # Convert date strings to datetime
        prospects_df['data_candidatura_dt'] = pd.to_datetime(
            prospects_df['data_candidatura'], 
            format='%d-%m-%Y', 
            errors='coerce'
        )
        
        # Group by date and count
        time_series = prospects_df.groupby(
            prospects_df['data_candidatura_dt'].dt.to_period('M')
        ).size().reset_index()
        
        time_series.columns = ['Mês', 'Candidaturas']
        time_series['Mês'] = time_series['Mês'].astype(str)
        
        # Create line chart
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
        # Distribution of job vacancies by area
        if 'areas_atuacao' in vagas_df.columns:
            # Split and count areas
            areas = vagas_df['areas_atuacao'].str.split('-').explode().str.strip()
            area_counts = areas.value_counts().head(10).reset_index()
            area_counts.columns = ['Área', 'Contagem']
            
            # Create horizontal bar chart
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
        
        # Distribution of job vacancies by location
        if 'estado' in vagas_df.columns and 'cidade' in vagas_df.columns:
            # Create a location column
            vagas_df['localização'] = vagas_df['cidade'] + ', ' + vagas_df['estado']
            
            # Count vacancies by location
            location_counts = vagas_df['localização'].value_counts().head(10).reset_index()
            location_counts.columns = ['Localização', 'Contagem']
            
            # Create horizontal bar chart
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
        
        # Distribution of job vacancies by academic level
        if 'nivel_academico' in vagas_df.columns:
            # Count vacancies by academic level
            academic_counts = vagas_df['nivel_academico'].value_counts().reset_index()
            academic_counts.columns = ['Nível Acadêmico', 'Contagem']
            
            # Create pie chart
            fig = px.pie(
                academic_counts,
                values='Contagem',
                names='Nível Acadêmico',
                title='Distribuição de Vagas por Nível Acadêmico'
            )
            
            st.plotly_chart(fig)
        
        # Distribution of job vacancies by English level
        if 'nivel_ingles' in vagas_df.columns:
            # Count vacancies by English level
            english_counts = vagas_df['nivel_ingles'].value_counts().reset_index()
            english_counts.columns = ['Nível de Inglês', 'Contagem']
            
            # Create pie chart
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
        # Distribution of candidates by area
        if 'area_atuacao' in applicants_df.columns:
            # Split and count areas
            applicants_df['area_atuacao'] = applicants_df['area_atuacao'].astype(str)
            areas = applicants_df['area_atuacao'].str.split(',').explode().str.strip()
            area_counts = areas.value_counts().head(10).reset_index()
            area_counts.columns = ['Área', 'Contagem']
            
            # Create horizontal bar chart
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
        
        # Distribution of candidates by academic level
        if 'nivel_academic' in applicants_df.columns:
            # Count candidates by academic level
            academic_counts = applicants_df['nivel_academic'].value_counts().reset_index()
            academic_counts.columns = ['Nível Acadêmico', 'Contagem']
            
            # Create pie chart
            fig = px.pie(
                academic_counts,
                values='Contagem',
                names='Nível Acadêmico',
                title='Distribuição de Candidatos por Nível Acadêmico'
            )
            
            st.plotly_chart(fig)
        
        # Distribution of candidates by English level
        if 'nivel_ingles' in applicants_df.columns:
            # Count candidates by English level
            english_counts = applicants_df['nivel_ingles'].value_counts().reset_index()
            english_counts.columns = ['Nível de Inglês', 'Contagem']
            
            # Create pie chart
            fig = px.pie(
                english_counts,
                values='Contagem',
                names='Nível de Inglês',
                title='Distribuição de Candidatos por Nível de Inglês'
            )
            
            st.plotly_chart(fig)
    
    # Process duration analysis
    if not prospects_df.empty and 'data_candidatura' in prospects_df.columns and 'ultima_atualizacao' in prospects_df.columns:
        # Convert date strings to datetime
        prospects_df['data_candidatura_dt'] = pd.to_datetime(
            prospects_df['data_candidatura'], 
            format='%d-%m-%Y', 
            errors='coerce'
        )
        
        prospects_df['ultima_atualizacao_dt'] = pd.to_datetime(
            prospects_df['ultima_atualizacao'], 
            format='%d-%m-%Y', 
            errors='coerce'
        )
        
        # Calculate duration in days
        prospects_df['duration'] = (
            prospects_df['ultima_atualizacao_dt'] - prospects_df['data_candidatura_dt']
        ).dt.days
        
        # Filter valid durations
        valid_duration = prospects_df[prospects_df['duration'] >= 0]
        
        if not valid_duration.empty:
            # Group by status and calculate average duration
            duration_by_status = valid_duration.groupby('situacao_candidado')['duration'].mean().reset_index()
            duration_by_status.columns = ['Status', 'Duração Média (dias)']
            
            # Create horizontal bar chart
            fig = px.bar(
                duration_by_status,
                y='Status',
                x='Duração Média (dias)',
                orientation='h',
                title='Duração Média do Processo por Status (dias)',
                labels={'Duração Média (dias)': 'Dias', 'Status': 'Status'},
                color='Duração Média (dias)',
                color_continuous_scale=px.colors.sequential.Oranges
            )
            
            st.plotly_chart(fig)

# Add filters and download options
st.sidebar.markdown("## Filtros")

# Date range filter for prospects
if not prospects_df.empty and 'data_candidatura' in prospects_df.columns:
    prospects_df['data_candidatura_dt'] = pd.to_datetime(
        prospects_df['data_candidatura'], 
        format='%d-%m-%Y', 
        errors='coerce'
    )
    
    min_date = prospects_df['data_candidatura_dt'].min().date()
    max_date = prospects_df['data_candidatura_dt'].max().date()
    
    date_range = st.sidebar.date_input(
        "Período de Candidatura",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_prospects = prospects_df[
            (prospects_df['data_candidatura_dt'].dt.date >= start_date) & 
            (prospects_df['data_candidatura_dt'].dt.date <= end_date)
        ]
        
        st.sidebar.markdown(f"**Candidaturas no período:** {len(filtered_prospects)}")

# Status filter
if not prospects_df.empty and 'situacao_candidado' in prospects_df.columns:
    all_statuses = ['Todos'] + sorted(prospects_df['situacao_candidado'].unique().tolist())
    selected_status = st.sidebar.selectbox("Status do Candidato", all_statuses)
    
    if selected_status != 'Todos':
        status_counts = prospects_df[prospects_df['situacao_candidado'] == selected_status].shape[0]
        st.sidebar.markdown(f"**Candidatos com status '{selected_status}':** {status_counts}")

# Download options
st.sidebar.markdown("## Download de Dados")

# Download vacancies
if not vagas_df.empty:
    csv_vagas = vagas_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Baixar Vagas (CSV)",
        data=csv_vagas,
        file_name="vagas_data.csv",
        mime="text/csv"
    )

# Download prospects
if not prospects_df.empty:
    csv_prospects = prospects_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Baixar Prospectos (CSV)",
        data=csv_prospects,
        file_name="prospects_data.csv",
        mime="text/csv"
    )

st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido para Decision/FIAP | © 2025")

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
