import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="HR Match - Documentation",
    page_icon="📝",
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

st.title("📝 Documentação")
st.markdown("### Sistema de Matching de Candidatos e Vagas")

# Conteúdo da documentação
st.markdown("""
## Sobre o Sistema

O Sistema de Matching de Candidatos e Vagas é uma ferramenta desenvolvida para a Decision. 

A Decision oferece serviços em Gestão de Recursos Humanos, atuando em Tecnologia da Informação, Projetos e Consultoria. Com tanto tempo no mercado, construímos um portfólio diverso, que envolve a oferta de Outsourcing, Hunting, BPO e BackOffice.

A ferramenta utiliza técnicas de Processamento de Linguagem Natural (NLP) e Aprendizado de Máquina para encontrar os candidatos mais adequados para cada vaga.

## Fluxo do Processo

1. **Carregamento de Dados**: O sistema carrega dados de três fontes principais:
   - `vagas.json`: Contém informações sobre as vagas disponíveis
   - `prospects.json`: Contém informações sobre os prospectos/candidaturas para cada vaga
   - `applicants.csv`: Contém informações detalhadas sobre os candidatos

2. **Processamento de Texto**: O sistema processa as descrições de vagas e perfis de candidatos utilizando técnicas de NLP:
   - Normalização de texto (remoção de acentos, conversão para minúsculas)
   - Remoção de stopwords e caracteres especiais
   - Extração de habilidades técnicas
   - Codificação vetorial utilizando modelos de embeddings

3. **Cálculo de Similaridade**: O sistema calcula a similaridade entre vagas e candidatos considerando:
   - Similaridade textual entre descrição da vaga e perfil do candidato
   - Comparação de habilidades técnicas
   - Match de formação acadêmica
   - Match de conhecimento de idiomas (inglês e espanhol)

4. **Apresentação dos Resultados**: Os resultados são apresentados em uma interface amigável, permitindo:
   - Visualização dos candidatos mais adequados para cada vaga
   - Visualização dos candidatos já inscritos em cada vaga
   - Análise estatística do processo de recrutamento

## Métricas de Match

O sistema utiliza as seguintes métricas para calcular a similaridade entre vagas e candidatos:

### 1. Similaridade Textual (35%)
Utiliza embeddings de sentenças para codificar descrições de vagas e perfis de candidatos em vetores, calculando a similaridade de cosseno entre eles.

### 2. Match de Competências (35%)
Extrai habilidades técnicas das descrições de vagas e perfis de candidatos, calculando a porcentagem de habilidades da vaga que o candidato possui.

### 3. Match de Formação (10%)
Compara o nível de formação exigido pela vaga com o nível de formação do candidato, atribuindo uma pontuação com base na adequação.

### 4. Match de Inglês (10%)
Compara o nível de inglês exigido pela vaga com o nível de inglês do candidato.

### 5. Match de Espanhol (10%)
Compara o nível de espanhol exigido pela vaga com o nível de espanhol do candidato.

## Ferramentas Utilizadas

- **Python**: Linguagem de programação principal
- **Streamlit**: Framework para criação da interface
- **NLTK**: Biblioteca para processamento de linguagem natural
- **Pandas**: Para manipulação de dados
- **Plotly**: Para visualização de dados

## Como Usar o Sistema

### Matching Tool (Ferramenta de Matching)

1. Acesse a aba "Matching Tool"
2. Selecione uma vaga no menu suspenso
3. Clique em "Buscar Candidatos" para encontrar os candidatos mais adequados
4. Analise os resultados, que incluem:
   - Pontuação geral e por categoria
   - Visualização gráfica das pontuações
   - Detalhes do perfil de cada candidato

Alternativamente, você pode:

1. Acessar a aba "Ver Candidatos Inscritos"
2. Selecionar uma vaga no menu suspenso
3. Clicar em "Ver Candidatos" para visualizar os candidatos já inscritos na vaga
4. Filtrar os resultados por situação do candidato

### Analytics (Análise)

1. Acesse a aba "Analytics"
2. Navegue pelas abas para visualizar diferentes tipos de análises:
   - Visão Geral: Métricas gerais do processo de recrutamento
   - Análise de Vagas: Estatísticas sobre as vagas disponíveis
   - Análise de Candidatos: Estatísticas sobre os candidatos

3. Utilize os filtros no painel lateral para refinar a análise
4. Baixe os dados em formato CSV se necessário

## Passo a Passo para Rodar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/Lucca-26/hr-recruitment-app.git
cd hr-recruitment-app
""")