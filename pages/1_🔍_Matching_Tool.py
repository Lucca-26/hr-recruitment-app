import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from helpers.data_loader import load_data, get_vaga_by_id
from helpers.text_processor import preprocess_text, extract_skills
from helpers.similarity_calculator import find_matching_candidates, get_candidates_by_vaga

# Configuração da página
st.set_page_config(
    page_title="HR Match - Matching Tool",
    page_icon="🔍",
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

st.title("🔍 Ferramenta de Matching")
st.markdown("### Encontre os candidatos mais adequados para cada vaga")

# Inicializar estado da sessão para dados, se ainda não estiver feito
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

# Criar abas para diferentes funcionalidades de matching
tab1, tab2 = st.tabs(["Buscar Candidatos para Vaga", "Ver Candidatos Inscritos"])

with tab1:
    st.markdown("### Buscar Candidatos para Vaga")
    
    # Seleção de vaga
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        vaga_selected = st.selectbox(
            "Selecione a vaga:",
            options=vagas_df['vaga_id'].tolist(),
            format_func=lambda x: f"{vagas_df[vagas_df['vaga_id'] == x]['titulo_vaga'].iloc[0]} ({x})"
        )
    
    with col2:
        top_n = st.slider("Número de candidatos a mostrar:", min_value=5, max_value=50, value=10, step=5)
        
    with col3:
        match_threshold = st.slider("Score mínimo de match (%):", min_value=0, max_value=100, value=50, step=5) / 100
    
    col4, col5 = st.columns([1, 1])
    with col4:
        show_top_match = st.checkbox("Mostrar apenas os candidatos mais aderentes", value=True, 
                                   help="Quando selecionado, mostra apenas os candidatos com maior score de similaridade")
    
    with col5:
        filter_by_skill = st.checkbox("Filtrar por competências técnicas", value=False,
                                   help="Prioriza candidatos com maior match em competências técnicas")
    
    if st.button("Buscar Candidatos"):
        with st.spinner("Analisando candidatos..."):
            # Obter informações da vaga
            job_data = vagas_df[vagas_df['vaga_id'] == vaga_selected].iloc[0]
            
            # Exibir informações da vaga
            with st.expander("Informações da Vaga", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Título:** {job_data['titulo_vaga']}")
                    st.markdown(f"**Cliente:** {job_data['cliente']}")
                    st.markdown(f"**Localização:** {job_data['cidade']}, {job_data['estado']}")
                    st.markdown(f"**Tipo de Contratação:** {job_data['tipo_contratacao']}")
                
                with col2:
                    st.markdown(f"**Nível Profissional:** {job_data['nivel_profissional']}")
                    st.markdown(f"**Nível Acadêmico:** {job_data['nivel_academico']}")
                    st.markdown(f"**Inglês:** {job_data['nivel_ingles']}")
                    st.markdown(f"**Espanhol:** {job_data['nivel_espanhol']}")
                
                st.markdown("**Área de Atuação:**")
                st.markdown(job_data['areas_atuacao'])
                
                st.markdown("**Principais Atividades:**")
                st.markdown(job_data['principais_atividades'])
                
                st.markdown("**Competências Técnicas e Comportamentais:**")
                st.markdown(job_data['competencia_tecnicas'])
            
            # Encontrar candidatos correspondentes
            # Buscar candidatos de acordo com os critérios selecionados
            matching_candidates = find_matching_candidates(
                vagas_df, applicants_df, vaga_selected, top_n=top_n if show_top_match else 100
            )
            
            if matching_candidates.empty:
                st.warning("Nenhum candidato adequado encontrado.")
            else:
                # Aplicar filtros adicionais conforme selecionado pelo usuário
                if match_threshold > 0:
                    matching_candidates = matching_candidates[matching_candidates['overall_score'] >= match_threshold]
                
                if filter_by_skill:
                    # Ordenar primeiro por skill_match e depois por overall_score
                    matching_candidates = matching_candidates.sort_values(['skill_match', 'overall_score'], ascending=[False, False])
                
                # Limitar ao número desejado
                if show_top_match and len(matching_candidates) > top_n:
                    matching_candidates = matching_candidates.head(top_n)
                
                # Verificar se ainda existem candidatos após os filtros
                if matching_candidates.empty:
                    st.warning("Nenhum candidato atende aos critérios de filtro selecionados.")
                else:
                    # Exibir resultados
                    st.markdown(f"### {len(matching_candidates)} Candidatos Recomendados")
                    st.success(f"Mostrando os candidatos mais aderentes à vaga com score mínimo de {match_threshold:.0%}")
                    
                    # Adicionar métricas de resumo
                    avg_score = matching_candidates['overall_score'].mean()
                    max_score = matching_candidates['overall_score'].max()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="Score Médio", value=f"{avg_score:.1%}")
                    with col2:
                        st.metric(label="Score Máximo", value=f"{max_score:.1%}")
                    with col3:
                        st.metric(label="Candidatos Encontrados", value=len(matching_candidates))
                
                # Criar gráfico radar para os 5 principais candidatos
                if len(matching_candidates) >= 5:
                    top_5_candidates = matching_candidates.head(5)
                    
                    # Preparar dados para o gráfico radar
                    categories = ['Similaridade Textual', 'Competências', 'Formação', 'Inglês', 'Espanhol']
                    
                    fig = px.line_polar(
                        r=[0, 0.25, 0.5, 0.75, 1],
                        theta=categories,
                        line_close=True,
                        range_r=[0, 1],
                        title="Comparação Top 5 Candidatos"
                    )
                    
                    for i, (_, candidate) in enumerate(top_5_candidates.iterrows()):
                        fig.add_trace(px.line_polar(
                            r=[
                                candidate['text_similarity'], 
                                candidate['skill_match'], 
                                candidate['education_match'],
                                candidate['english_match'],
                                candidate['spanish_match']
                            ],
                            theta=categories,
                            line_close=True,
                            range_r=[0, 1]
                        ).data[0])
                    
                    fig.update_traces(fill='toself')
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 1]
                            )
                        ),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig)
                
                # Exibir tabela de candidatos
                formatted_candidates = matching_candidates.copy()
                
                # Formatar pontuações como percentuais
                score_columns = ['overall_score', 'text_similarity', 'skill_match', 
                                'education_match', 'english_match', 'spanish_match']
                
                for col in score_columns:
                    formatted_candidates[col] = formatted_candidates[col].apply(lambda x: f"{x:.1%}")
                
                # Renomear colunas para exibição
                formatted_candidates = formatted_candidates.rename(columns={
                    'codigo': 'Código',
                    'nome': 'Nome',
                    'area_atuacao': 'Área de Atuação',
                    'nivel_academico': 'Formação Acadêmica',
                    'nivel_ingles': 'Nível de Inglês',
                    'nivel_espanhol': 'Nível de Espanhol',
                    'overall_score': 'Pontuação Geral',
                    'text_similarity': 'Similaridade Textual',
                    'skill_match': 'Competências',
                    'education_match': 'Match Formação',
                    'english_match': 'Match Inglês',
                    'spanish_match': 'Match Espanhol'
                })
                
                st.dataframe(formatted_candidates)
                
                # Visão detalhada de cada candidato
                for i, (_, candidate) in enumerate(matching_candidates.iterrows()):
                    with st.expander(f"{i+1}. {candidate['nome']} - {candidate['overall_score']:.1%}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Código:** {candidate['codigo']}")
                            st.markdown(f"**Nome:** {candidate['nome']}")
                            st.markdown(f"**Área de Atuação:** {candidate['area_atuacao']}")
                            st.markdown(f"**Formação:** {candidate['nivel_academico']}")
                        
                        with col2:
                            st.markdown(f"**Pontuação Geral:** {candidate['overall_score']:.1%}")
                            st.markdown(f"**Similaridade Textual:** {candidate['text_similarity']:.1%}")
                            st.markdown(f"**Match de Competências:** {candidate['skill_match']:.1%}")
                            st.markdown(f"**Match de Formação:** {candidate['education_match']:.1%}")
                            st.markdown(f"**Match de Inglês:** {candidate['english_match']:.1%}")
                            st.markdown(f"**Match de Espanhol:** {candidate['spanish_match']:.1%}")
                        
                        # Encontrar perfil do candidato nos dados de candidatos
                        candidate_profile = applicants_df[applicants_df['codigo_profissional'] == candidate['codigo']]
                        
                        if not candidate_profile.empty:
                            profile = candidate_profile.iloc[0]
                            
                            st.markdown("**Perfil Profissional:**")
                            st.markdown(profile.get('titulo_profissional', ''))
                            
                            st.markdown("**Conhecimentos Técnicos:**")
                            st.markdown(profile.get('conhecimentos_tecnicos', ''))
                            
                            st.markdown("**Certificações:**")
                            st.markdown(profile.get('certificacoes', ''))
                
                # Opções de download
                st.markdown("### Download dos Resultados")
                
                csv = matching_candidates.to_csv(index=False)
                st.download_button(
                    label="Baixar como CSV",
                    data=csv,
                    file_name=f"candidatos_vaga_{vaga_selected}.csv",
                    mime="text/csv"
                )

with tab2:
    st.markdown("### Ver Candidatos Inscritos")
    
    # Seleção de vaga
    vaga_selected_2 = st.selectbox(
        "Selecione a vaga:",
        options=vagas_df['vaga_id'].tolist(),
        format_func=lambda x: f"{vagas_df[vagas_df['vaga_id'] == x]['titulo_vaga'].iloc[0]} ({x})",
        key="vaga_selectbox_2"
    )
    
    if st.button("Ver Candidatos"):
        with st.spinner("Buscando candidatos inscritos..."):
            # Obter informações da vaga
            job_data = vagas_df[vagas_df['vaga_id'] == vaga_selected_2].iloc[0]
            
            # Exibir informações da vaga
            with st.expander("Informações da Vaga", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Título:** {job_data['titulo_vaga']}")
                    st.markdown(f"**Cliente:** {job_data['cliente']}")
                    st.markdown(f"**Localização:** {job_data['cidade']}, {job_data['estado']}")
                    st.markdown(f"**Tipo de Contratação:** {job_data['tipo_contratacao']}")
                
                with col2:
                    st.markdown(f"**Nível Profissional:** {job_data['nivel_profissional']}")
                    st.markdown(f"**Nível Acadêmico:** {job_data['nivel_academico']}")
                    st.markdown(f"**Inglês:** {job_data['nivel_ingles']}")
                    st.markdown(f"**Espanhol:** {job_data['nivel_espanhol']}")
            
            # Obter candidatos para esta vaga
            candidates = get_candidates_by_vaga(
                vagas_df, prospects_df, applicants_df, vaga_selected_2
            )
            
            if candidates.empty:
                st.warning("Nenhum candidato inscrito para esta vaga.")
            else:
                # Exibir candidatos
                st.markdown(f"### Candidatos Inscritos: {len(candidates)}")
                
                # Formatar tabela de candidatos
                formatted_candidates = candidates.copy()
                
                # Formatar pontuações como percentuais se existirem
                score_columns = ['overall_score', 'text_similarity', 'skill_match', 
                                'education_match', 'english_match', 'spanish_match']
                
                for col in score_columns:
                    if col in formatted_candidates.columns:
                        formatted_candidates[col] = formatted_candidates[col].apply(lambda x: f"{x:.1%}")
                
                # Renomear colunas para exibição
                columns_mapping = {
                    'codigo': 'Código',
                    'nome': 'Nome',
                    'area_atuacao': 'Área de Atuação',
                    'nivel_academico': 'Formação Acadêmica',
                    'nivel_ingles': 'Nível de Inglês',
                    'nivel_espanhol': 'Nível de Espanhol',
                    'situacao': 'Situação',
                    'data_candidatura': 'Data de Candidatura',
                    'recrutador': 'Recrutador',
                    'overall_score': 'Pontuação Geral',
                    'text_similarity': 'Similaridade Textual',
                    'skill_match': 'Competências',
                    'education_match': 'Match Formação',
                    'english_match': 'Match Inglês',
                    'spanish_match': 'Match Espanhol'
                }
                
                formatted_candidates = formatted_candidates.rename(columns={
                    k: v for k, v in columns_mapping.items() if k in formatted_candidates.columns
                })
                
                st.dataframe(formatted_candidates)
                
                # Opções de download
                csv = candidates.to_csv(index=False)
                st.download_button(
                    label="Baixar como CSV",
                    data=csv,
                    file_name=f"candidatos_inscritos_vaga_{vaga_selected_2}.csv",
                    mime="text/csv"
                )

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