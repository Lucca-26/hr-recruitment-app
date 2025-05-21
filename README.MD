# HR Recruitment App

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python 3.9+"/>
  <img src="https://img.shields.io/badge/Streamlit-1.30+-red.svg" alt="Streamlit 1.30+"/>
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"/>
</div>

<p align="center">Uma aplicação de recrutamento baseada em IA que usa processamento de linguagem natural para encontrar os candidatos mais adequados para vagas de emprego.</p>

<p align="center">
  <a href="#sobre">Sobre</a> •
  <a href="#funcionalidades">Funcionalidades</a> •
  <a href="#demonstração">Demonstração</a> •
  <a href="#instalação">Instalação</a> •
  <a href="#deploy">Deploy</a> •
  <a href="#tecnologias">Tecnologias</a> •
  <a href="#estrutura">Estrutura</a> •
  <a href="#contribuições">Contribuições</a> •
  <a href="#licença">Licença</a>
</p>

## 📋 Sobre

O HR Recruitment App é uma ferramenta desenvolvida para a Decision/FIAP. A aplicação usa técnicas de processamento de linguagem natural (NLP) para analisar perfis de candidatos e descrições de vagas, calculando scores de compatibilidade com base em múltiplos fatores.

A Decision oferece serviços em Gestão de Recursos Humanos, atuando em Tecnologia da Informação, Projetos e Consultoria. Com tanto tempo no mercado, construímos um portfólio diverso, que envolve a oferta de Outsourcing, Hunting, BPO e BackOffice.

## ✨ Funcionalidades

- **Matching de Candidatos**: Encontre candidatos com perfil mais adequado para suas vagas
- **Análise de Perfis**: Visualize a compatibilidade entre candidatos e vagas por diferentes critérios
- **Dashboards Analíticos**: Obtenha insights sobre o processo de recrutamento
- **Filtros Avançados**: Refine sua busca com filtros de pontuação mínima e competências técnicas
- **Interface Intuitiva**: Design amigável e responsivo para facilitar a navegação

## 🎬 Demonstração

A aplicação está disponível online em: [https://hr-recruitment-app.streamlit.app](https://hr-recruitment-app.streamlit.app)

![HR Recruitment App Screenshot](screenshot.png)

## 🚀 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- Git

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/hr-recruitment-app.git
cd hr-recruitment-app

# Crie e ative um ambiente virtual
python -m venv venv

# No Windows:
venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Baixe os recursos do NLTK
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Execute a aplicação
streamlit run app.py
```

Após estes comandos, a aplicação estará disponível em:
- URL local: http://localhost:8501
- URL de rede: http://seu-ip:8501

## 🌐 Deploy

### Deploy no Streamlit Cloud

1. **Prepare seu repositório**:
   - Certifique-se de que seu repositório contém todos os arquivos necessários
   - Verifique se `requirements.txt` está atualizado
   - Confirme se `.streamlit/config.toml` está configurado corretamente

2. **Crie uma conta Streamlit Cloud**:
   - Acesse [Streamlit Cloud](https://streamlit.io/cloud)
   - Faça login com GitHub, Google ou e-mail

3. **Crie um novo app**:
   - Clique em "New app"
   - Selecione seu repositório GitHub
   - Especifique a branch (geralmente "main")
   - Defina "Main file path" como "app.py"
   - Clique em "Deploy"

4. **Configurações avançadas (opcional)**:
   - Configure segredos, se necessário
   - Defina recursos de computação
   - Configure domínio personalizado

5. **Acesse seu app**:
   - Após a implantação, seu app estará disponível em uma URL como:
     `https://username-hr-recruitment-app-app-xxxx.streamlit.app`

### Deploy com Docker

```bash
# Construa a imagem Docker
docker build -t hr-recruitment-app .

# Execute o contêiner
docker run -p 8501:8501 hr-recruitment-app
```

## 🔧 Tecnologias

- **Python**: Linguagem de programação principal
- **Streamlit**: Framework para interface web
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica
- **NLTK**: Processamento de linguagem natural
- **Scikit-learn**: Algoritmos de machine learning
- **Plotly**: Visualizações interativas

## 📁 Estrutura

```
hr-recruitment-app/
├── app.py                   # Arquivo principal da aplicação
├── helpers/                 # Módulos auxiliares
│   ├── __init__.py          # Torna o diretório um pacote Python
│   ├── data_loader.py       # Carregamento de dados
│   ├── similarity_calculator.py # Cálculo de similaridade
│   └── text_processor.py    # Processamento de texto
├── pages/                   # Páginas da aplicação
│   ├── 1_🔍_Matching_Tool.py   # Ferramenta de matching
│   ├── 2_📊_Analytics.py     # Visualizações analíticas
│   └── 3_📝_Documentation.py  # Documentação
├── .streamlit/              # Configurações do Streamlit
│   └── config.toml          # Configurações de servidor
├── vagas.json               # Dados de vagas
├── prospects.json           # Dados de candidaturas
├── applicants.csv           # Dados de candidatos
├── requirements.txt         # Dependências do projeto
├── README.md                # Este arquivo
├── .gitignore               # Arquivos ignorados pelo Git
└── LICENSE                  # Licença MIT
```

## 📊 Datasets

A aplicação utiliza três conjuntos de dados:
- `vagas.json`: Informações sobre vagas de emprego
- `prospects.json`: Dados de candidaturas para vagas específicas
- `applicants.csv`: Informações detalhadas sobre candidatos

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

## 👥 Autores

**Grupo 9 | 6DTAT:**
- Francisco das Chagas Alcântara Júnior – RM 357554
- Geovana Façanha da Silva – RM357215
- Luciana Conceição Ferreira – RM357220

---

<p align="center">Desenvolvido para Decision/FIAP | © 2025</p>