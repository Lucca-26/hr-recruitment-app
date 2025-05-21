import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from helpers.text_processor import preprocess_text, encode_text
from helpers.data_loader import get_applicant_by_code, get_vaga_by_id, get_prospects_by_vaga

def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calcula a similaridade de cosseno entre dois vetores.
    
    Args:
        vec1: Primeiro vetor
        vec2: Segundo vetor
    
    Returns:
        Pontuação de similaridade de cosseno entre 0 e 1
    """
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)

def calculate_skill_overlap(job_text: str, candidate_text: str) -> float:
    """
    Calcula a sobreposição entre habilidades da vaga e habilidades do candidato.
    
    Args:
        job_text: Texto descritivo da vaga ou requisitos
        candidate_text: Texto do perfil ou currículo do candidato
    
    Returns:
        Pontuação representando a sobreposição de habilidades entre 0 e 1
    """
    # Pré-processar textos
    job_processed = preprocess_text(job_text)
    candidate_processed = preprocess_text(candidate_text)
    
    # Se algum texto estiver vazio, retorna 0
    if not job_processed or not candidate_processed:
        return 0.0
    
    # Dividir em palavras (simplificado)
    job_words = set(job_processed.split())
    candidate_words = set(candidate_processed.split())
    
    # Calcular sobreposição
    common_words = job_words.intersection(candidate_words)
    
    if not job_words:
        return 0.0
    
    # Pontuação baseada na proporção de palavras da vaga presentes no perfil do candidato
    return len(common_words) / len(job_words)

def calculate_education_level_match(job_level: str, candidate_level: str) -> float:
    """
    Calcula pontuação de match com base nos níveis de educação.
    
    Args:
        job_level: Nível de educação exigido para a vaga
        candidate_level: Nível de educação do candidato
    
    Returns:
        Pontuação de match educacional entre 0 e 1
    """
    # Nivelar para comparação
    job_level = job_level.lower() if job_level else ""
    candidate_level = candidate_level.lower() if candidate_level else ""
    
    # Definir hierarquia de níveis educacionais
    levels = {
        'ensino médio': 1,
        'técnico': 2,
        'graduação': 3,
        'superior': 3,
        'pós-graduação': 4,
        'especialização': 4,
        'mba': 4,
        'mestrado': 5,
        'doutorado': 6,
        'phd': 6
    }
    
    # Atribuir valores com base nas palavras-chave presentes
    job_value = 0
    candidate_value = 0
    
    for level, value in levels.items():
        if level in job_level:
            job_value = max(job_value, value)
        if level in candidate_level:
            candidate_value = max(candidate_value, value)
    
    # Se não há requisito educacional, pontuação máxima
    if job_value == 0:
        return 1.0
    
    # Se o candidato atende ou excede o requisito
    if candidate_value >= job_value:
        return 1.0
    
    # Caso contrário, pontuação parcial
    return candidate_value / job_value

def calculate_language_match(job_language_level: str, candidate_language_level: str) -> float:
    """
    Calcula pontuação de match com base nos níveis de proficiência em idiomas.
    
    Args:
        job_language_level: Nível de idioma exigido para a vaga
        candidate_language_level: Nível de idioma do candidato
    
    Returns:
        Pontuação de match de idioma entre 0 e 1
    """
    # Nivelar para comparação
    job_level = job_language_level.lower() if job_language_level else "não exigido"
    candidate_level = candidate_language_level.lower() if candidate_language_level else "não possui"
    
    # Definir hierarquia de níveis de idioma
    levels = {
        'não exigido': 0,
        'não possui': 0,
        'básico': 1,
        'intermediário': 2,
        'avançado': 3,
        'fluente': 4
    }
    
    # Atribuir valores com base nas palavras-chave presentes
    job_value = 0
    candidate_value = 0
    
    for level, value in levels.items():
        if level in job_level:
            job_value = max(job_value, value)
        if level in candidate_level:
            candidate_value = max(candidate_value, value)
    
    # Se não há requisito de idioma, pontuação máxima
    if job_value == 0:
        return 1.0
    
    # Se o candidato atende ou excede o requisito
    if candidate_value >= job_value:
        return 1.0
    
    # Caso contrário, pontuação parcial
    return candidate_value / job_value

def calculate_similarity(job_data: pd.Series, candidate_data: pd.Series) -> Dict[str, float]:
    """
    Calcula a similaridade geral entre uma vaga e um candidato.
    
    Args:
        job_data: Series contendo dados da vaga
        candidate_data: Series contendo dados do candidato
    
    Returns:
        Dicionário com pontuações de similaridade por categoria e pontuação geral
    """
    # Extrair textos relevantes
    job_description = " ".join([
        str(job_data.get('titulo_vaga', '')),
        str(job_data.get('areas_atuacao', '')),
        str(job_data.get('principais_atividades', '')),
        str(job_data.get('competencia_tecnicas', ''))
    ])
    
    candidate_description = " ".join([
        str(candidate_data.get('titulo_profissional', '')),
        str(candidate_data.get('area_atuacao', '')),
        str(candidate_data.get('conhecimentos_tecnicos', '')),
        str(candidate_data.get('certificacoes', ''))
    ])
    
    # Calcular similaridade textual
    job_vector = encode_text(job_description)
    candidate_vector = encode_text(candidate_description)
    text_similarity = calculate_cosine_similarity(job_vector, candidate_vector)
    
    # Calcular similaridade de competências
    skill_match = calculate_skill_overlap(
        job_data.get('competencia_tecnicas', ''),
        candidate_data.get('conhecimentos_tecnicos', '')
    )
    
    # Calcular match de formação acadêmica
    education_match = calculate_education_level_match(
        job_data.get('nivel_academico', ''),
        candidate_data.get('nivel_academico', '')
    )
    
    # Calcular match de inglês
    english_match = calculate_language_match(
        job_data.get('nivel_ingles', 'não exigido'),
        candidate_data.get('nivel_ingles', 'não possui')
    )
    
    # Calcular match de espanhol
    spanish_match = calculate_language_match(
        job_data.get('nivel_espanhol', 'não exigido'),
        candidate_data.get('nivel_espanhol', 'não possui')
    )
    
    # Calcular pontuação geral (com pesos)
    weights = {
        'text_similarity': 0.35,
        'skill_match': 0.35,
        'education_match': 0.10,
        'english_match': 0.10,
        'spanish_match': 0.10
    }
    
    overall_score = (
        weights['text_similarity'] * text_similarity +
        weights['skill_match'] * skill_match +
        weights['education_match'] * education_match +
        weights['english_match'] * english_match +
        weights['spanish_match'] * spanish_match
    )
    
    return {
        'overall_score': overall_score,
        'text_similarity': text_similarity,
        'skill_match': skill_match,
        'education_match': education_match,
        'english_match': english_match,
        'spanish_match': spanish_match
    }

def find_matching_candidates(vagas_df: pd.DataFrame, applicants_df: pd.DataFrame, vaga_id: str, 
                             top_n: int = 10) -> pd.DataFrame:
    """
    Encontra os top N candidatos mais adequados para uma vaga específica.
    
    Args:
        vagas_df: DataFrame com vagas
        applicants_df: DataFrame com dados de candidatos
        vaga_id: ID da vaga para correspondência
        top_n: Número de candidatos principais a retornar
    
    Returns:
        DataFrame com candidatos principais e suas pontuações
    """
    # Obter dados da vaga
    job_series = vagas_df[vagas_df['vaga_id'] == vaga_id].iloc[0]
    
    # Calcular similaridade para cada candidato
    results = []
    
    for _, candidate in applicants_df.iterrows():
        # Calcular similaridade
        similarity_scores = calculate_similarity(job_series, candidate)
        
        # Adicionar dados do candidato e pontuações ao resultado
        candidate_data = {
            'codigo': candidate['codigo_profissional'],
            'nome': candidate['nome_profissional'],
            'area_atuacao': candidate['area_atuacao'],
            'nivel_academico': candidate['nivel_academico'],
            'nivel_ingles': candidate['nivel_ingles'],
            'nivel_espanhol': candidate['nivel_espanhol'],
            'overall_score': similarity_scores['overall_score'],
            'text_similarity': similarity_scores['text_similarity'],
            'skill_match': similarity_scores['skill_match'],
            'education_match': similarity_scores['education_match'],
            'english_match': similarity_scores['english_match'],
            'spanish_match': similarity_scores['spanish_match']
        }
        
        results.append(candidate_data)
    
    # Criar DataFrame e ordenar por pontuação geral
    if results:
        result_df = pd.DataFrame(results)
        result_df = result_df.sort_values('overall_score', ascending=False)
        
        # Limitar para os top N candidatos
        if len(result_df) > top_n:
            result_df = result_df.head(top_n)
        
        return result_df
    else:
        # Retornar DataFrame vazio se não houver resultados
        return pd.DataFrame()

def get_candidates_by_vaga(vagas_df: pd.DataFrame, prospects_df: pd.DataFrame, applicants_df: pd.DataFrame, 
                           vaga_id: str, include_scores: bool = True) -> pd.DataFrame:
    """
    Obtém todos os candidatos que se candidataram a uma vaga específica com pontuações de similaridade.
    
    Args:
        vagas_df: DataFrame com vagas
        prospects_df: DataFrame com dados de prospectos
        applicants_df: DataFrame com dados de candidatos
        vaga_id: ID da vaga para obter candidatos
        include_scores: Se deve incluir pontuações de similaridade
    
    Returns:
        DataFrame com candidatos e suas informações
    """
    # Obter prospectos para a vaga
    vaga_prospects = prospects_df[prospects_df['vaga_id'] == vaga_id]
    
    if vaga_prospects.empty:
        return pd.DataFrame()
    
    # Obter dados da vaga
    job_series = vagas_df[vagas_df['vaga_id'] == vaga_id].iloc[0]
    
    # Preparar resultados
    results = []
    
    for _, prospect in vaga_prospects.iterrows():
        # Obter dados do candidato
        candidate_code = prospect['codigo']
        candidate_row = applicants_df[applicants_df['codigo_profissional'] == candidate_code]
        
        if candidate_row.empty:
            continue
        
        candidate = candidate_row.iloc[0]
        
        # Base de dados do candidato
        candidate_data = {
            'codigo': candidate['codigo_profissional'],
            'nome': candidate['nome_profissional'],
            'area_atuacao': candidate['area_atuacao'],
            'nivel_academico': candidate['nivel_academico'],
            'nivel_ingles': candidate['nivel_ingles'],
            'nivel_espanhol': candidate['nivel_espanhol'],
            'situacao': prospect['situacao_candidado'],
            'data_candidatura': prospect['data_candidatura'],
            'recrutador': prospect.get('recrutador', '')
        }
        
        # Adicionar pontuações se solicitado
        if include_scores:
            similarity_scores = calculate_similarity(job_series, candidate)
            candidate_data.update({
                'overall_score': similarity_scores['overall_score'],
                'text_similarity': similarity_scores['text_similarity'],
                'skill_match': similarity_scores['skill_match'],
                'education_match': similarity_scores['education_match'],
                'english_match': similarity_scores['english_match'],
                'spanish_match': similarity_scores['spanish_match']
            })
        
        results.append(candidate_data)
    
    # Criar DataFrame e ordenar
    if results:
        result_df = pd.DataFrame(results)
        if include_scores and 'overall_score' in result_df.columns:
            result_df = result_df.sort_values('overall_score', ascending=False)
        return result_df
    else:
        # Retornar DataFrame vazio se não houver resultados
        return pd.DataFrame()