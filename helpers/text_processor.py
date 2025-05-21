import re
import unicodedata
import numpy as np
import pandas as pd
import streamlit as st
import nltk
from typing import List

# Download de recursos do NLTK
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Stopwords para remover durante o processamento
STOPWORDS = {
    'portuguese': ['a', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'até', 
                  'com', 'como', 'da', 'das', 'de', 'dela', 'delas', 'dele', 'deles', 'depois',
                  'do', 'dos', 'e', 'ela', 'elas', 'ele', 'eles', 'em', 'entre', 'era', 'eram', 
                  'essa', 'essas', 'esse', 'esses', 'esta', 'estas', 'este', 'estes', 'eu',
                  'foi', 'foram', 'isso', 'isto', 'já', 'lhe', 'lhes', 'mais', 'mas', 'me', 
                  'mesmo', 'meu', 'meus', 'minha', 'minhas', 'muito', 'na', 'não', 'nas', 'nem', 
                  'no', 'nos', 'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'num', 'numa', 'o', 
                  'os', 'ou', 'para', 'pela', 'pelas', 'pelo', 'pelos', 'por', 'qual', 'quando', 
                  'que', 'quem', 'se', 'sem', 'seu', 'seus', 'só', 'sua', 'suas', 'também', 
                  'te', 'teu', 'tua', 'tuas', 'teus', 'um', 'uma', 'você', 'vocês']
}

# Classe para geração de embeddings
class SimpleEmbedder:
    """Implementação simplificada de modelo de embedding para processamento de texto"""
    
    def encode(self, texts):
        """
        Codifica textos em vetores de embedding simplificados
        
        Args:
            texts: String única ou lista de strings para codificar
            
        Returns:
            Vetor de embedding único ou array de vetores
        """
        if isinstance(texts, str):
            texts = [texts]
        
        # Cria vetores simples baseados nos caracteres do texto
        results = []
        for text in texts:
            # Cria um vetor de 384 dimensões (simulando o tamanho de embeddings reais)
            text_bytes = text.encode('utf-8')
            vec = np.zeros(384)
            for i, byte in enumerate(text_bytes[:384]):
                vec[i % 384] += byte / 255.0
            
            # Normaliza o vetor
            if np.linalg.norm(vec) > 0:
                vec = vec / np.linalg.norm(vec)
            results.append(vec)
        
        if len(results) == 1:
            return results[0]
        return np.array(results)

# Cache do modelo de embedding
@st.cache_resource
def load_embedding_model():
    """
    Uma versão simplificada do modelo de embeddings.
    
    Returns:
        Um objeto simulado que usa embedding baseado em caracteres
    """
    return SimpleEmbedder()

def preprocess_text(text: str, language: str = 'portuguese') -> str:
    """
    Pré-processa o texto removendo caracteres especiais, padronizando espaços
    e convertendo para minúsculas.
    
    Args:
        text: Texto a ser pré-processado
        language: Idioma para stopwords (padrão: 'portuguese')
    
    Returns:
        Texto pré-processado
    """
    if pd.isna(text) or text is None:
        return ""
    
    # Converte para minúsculas
    text = text.lower()
    
    # Remove acentos
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    
    # Substitui quebras de linha por espaços
    text = re.sub(r'\n', ' ', text)
    
    # Remove caracteres especiais
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Normaliza espaços
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_skills(text: str) -> List[str]:
    """
    Extrai habilidades técnicas do texto.
    Usa uma abordagem simples de correspondência de palavras-chave.
    
    Args:
        text: Texto para extrair habilidades
    
    Returns:
        Lista de habilidades extraídas
    """
    # Lista de habilidades técnicas comuns (exemplo simplificado)
    common_skills = [
        'python', 'java', 'javascript', 'html', 'css', 'sql', 'react', 'angular',
        'node', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'devops', 'ci/cd',
        'git', 'agile', 'scrum', 'kanban', 'nosql', 'mongodb', 'postgresql', 'mysql',
        'oracle', 'data science', 'machine learning', 'deep learning', 'ai', 'nlp',
        'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn', 'big data',
        'hadoop', 'spark', 'tableau', 'power bi', 'excel', 'word', 'powerpoint',
        'photoshop', 'illustrator', 'indesign', 'figma', 'sketch', 'xd'
    ]
    
    # Pré-processar o texto
    processed_text = preprocess_text(text)
    
    # Extrair habilidades
    found_skills = []
    for skill in common_skills:
        if skill in processed_text:
            found_skills.append(skill)
    
    return found_skills

def encode_text(text: str) -> np.ndarray:
    """
    Codifica o texto em uma representação vetorial usando um modelo pré-treinado.
    
    Args:
        text: Texto a ser codificado
    
    Returns:
        Representação vetorial do texto
    """
    # Carrega o modelo de embedding
    model = load_embedding_model()
    
    # Pré-processa o texto
    processed_text = preprocess_text(text)
    
    # Codifica o texto usando o modelo
    vector = model.encode(processed_text)
    
    return vector

def encode_dataframe_column(df: pd.DataFrame, column_name: str, new_column_name: str = "") -> pd.DataFrame:
    """
    Codifica uma coluna de texto em um DataFrame em representações vetoriais.
    
    Args:
        df: DataFrame contendo a coluna de texto
        column_name: Nome da coluna a ser codificada
        new_column_name: Nome da nova coluna para armazenar as codificações
    
    Returns:
        DataFrame com coluna de codificação vetorial adicionada
    """
    if new_column_name == "":
        new_column_name = f"{column_name}_vector"
    
    # Copia o DataFrame para não modificar o original
    df_copy = df.copy()
    
    # Codifica cada texto na coluna
    vectors = []
    for text in df[column_name]:
        vectors.append(encode_text(text))
    
    # Adiciona os vetores como uma nova coluna
    df_copy[new_column_name] = vectors
    
    return df_copy