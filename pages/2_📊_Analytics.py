import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from helpers.text_processor import encode_text, preprocess_text, extract_skills

def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
    
    Returns:
        Cosine similarity score between 0 and 1
    """
    if vec1.ndim == 1:
        vec1 = vec1.reshape(1, -1)
    if vec2.ndim == 1:
        vec2 = vec2.reshape(1, -1)
    
    return cosine_similarity(vec1, vec2)[0][0]

def calculate_skill_overlap(job_text: str, candidate_text: str) -> float:
    """
    Calculate the overlap between job skills and candidate skills.
    
    Args:
        job_text: Job description or requirements text
        candidate_text: Candidate profile or resume text
    
    Returns:
        Score representing the overlap of skills between 0 and 1
    """
    job_skills = set(extract_skills(job_text))
    candidate_skills = set(extract_skills(candidate_text))
    
    if not job_skills or not candidate_skills:
        return 0.0
    
    # Calculate overlap
    overlap = len(job_skills.intersection(candidate_skills))
    denominator = len(job_skills)
    
    if denominator == 0:
        return 0.0
    
    return overlap / denominator

def calculate_education_level_match(job_level: str, candidate_level: str) -> float:
    """
    Calculate match score based on education levels.
    
    Args:
        job_level: Required education level for the job
        candidate_level: Candidate's education level
    
    Returns:
        Education match score between 0 and 1
    """
    education_levels = {
        'ensino fundamental': 1,
        'ensino médio': 2,
        'ensino médio completo': 2,
        'ensino técnico': 3,
        'ensino técnico completo': 3,
        'ensino superior': 4,
        'ensino superior cursando': 4,
        'ensino superior incompleto': 4,
        'ensino superior completo': 5,
        'pós-graduação': 6,
        'especialização': 6,
        'mba': 6,
        'mestrado': 7,
        'doutorado': 8
    }
    
    # Normalize inputs to lowercase
    job_level_lower = job_level.lower() if isinstance(job_level, str) else ''
    candidate_level_lower = candidate_level.lower() if isinstance(candidate_level, str) else ''
    
    # Get education level integers or default to 0
    job_level_num = 0
    candidate_level_num = 0
    
    for level, value in education_levels.items():
        if level in job_level_lower:
            job_level_num = value
        if level in candidate_level_lower:
            candidate_level_num = value
    
    # If no education requirement for job, return 1.0 (match)
    if job_level_num == 0:
        return 1.0
    
    # If candidate meets or exceeds the job requirement
    if candidate_level_num >= job_level_num:
        return 1.0
    
    # If candidate is below the requirement, partial match based on how close
    return candidate_level_num / job_level_num if job_level_num > 0 else 0.0

def calculate_language_match(job_language_level: str, candidate_language_level: str) -> float:
    """
    Calculate match score based on language proficiency levels.
    
    Args:
        job_language_level: Required language level for the job
        candidate_language_level: Candidate's language proficiency level
    
    Returns:
        Language match score between 0 and 1
    """
    language_levels = {
        'nenhum': 0,
        'básico': 1,
        'intermediário': 2,
        'avançado': 3,
        'fluente': 4
    }
    
    # Normalize inputs to lowercase
    job_level_lower = job_language_level.lower() if isinstance(job_language_level, str) else ''
    candidate_level_lower = candidate_language_level.lower() if isinstance(candidate_language_level, str) else ''
    
    # Get language level integers or default to 0
    job_level_num = 0
    candidate_level_num = 0
    
    for level, value in language_levels.items():
        if level in job_level_lower:
            job_level_num = value
        if level in candidate_level_lower:
            candidate_level_num = value
    
    # If no language requirement for job, return 1.0 (match)
    if job_level_num == 0:
        return 1.0
    
    # If candidate meets or exceeds the job requirement
    if candidate_level_num >= job_level_num:
        return 1.0
    
    # If candidate is below the requirement, partial match based on how close
    return candidate_level_num / job_level_num if job_level_num > 0 else 0.0

def calculate_similarity(job_data: pd.Series, candidate_data: pd.Series) -> Dict[str, float]:
    """
    Calculate overall similarity between a job and a candidate.
    
    Args:
        job_data: Series containing job data
        candidate_data: Series containing candidate data
    
    Returns:
        Dictionary with similarity scores by category and overall score
    """
    # Handle missing values
    job_description = job_data.get('descricao_completa', '')
    if not isinstance(job_description, str):
        job_description = ''
    
    candidate_profile = candidate_data.get('profile_text', '')
    if not isinstance(candidate_profile, str):
        candidate_profile = ''
    
    # Calculate text similarity using embeddings
    job_vector = encode_text(job_description)
    candidate_vector = encode_text(candidate_profile)
    text_similarity = calculate_cosine_similarity(job_vector, candidate_vector)
    
    # Calculate skill overlap
    skill_match = calculate_skill_overlap(job_description, candidate_profile)
    
    # Obter valores garantindo que sejam strings
    job_nivel_academico = job_data.get('nivel_academico', '')
    if job_nivel_academico is None:
        job_nivel_academico = ''
        
    candidate_nivel_academico = candidate_data.get('nivel_academic', '')
    if candidate_nivel_academico is None:
        candidate_nivel_academico = ''
    
    # Calculate education match
    education_match = calculate_education_level_match(
        job_nivel_academico, 
        candidate_nivel_academico
    )
    
    # Obter valores garantindo que sejam strings
    job_nivel_ingles = job_data.get('nivel_ingles', '')
    if job_nivel_ingles is None:
        job_nivel_ingles = ''
        
    candidate_nivel_ingles = candidate_data.get('nivel_ingles', '')
    if candidate_nivel_ingles is None:
        candidate_nivel_ingles = ''
    
    # Calculate English language match
    english_match = calculate_language_match(
        job_nivel_ingles, 
        candidate_nivel_ingles
    )
    
    # Obter valores garantindo que sejam strings
    job_nivel_espanhol = job_data.get('nivel_espanhol', '')
    if job_nivel_espanhol is None:
        job_nivel_espanhol = ''
        
    candidate_nivel_espanhol = candidate_data.get('nivel_espanhol', '')
    if candidate_nivel_espanhol is None:
        candidate_nivel_espanhol = ''
    
    # Calculate Spanish language match
    spanish_match = calculate_language_match(
        job_nivel_espanhol, 
        candidate_nivel_espanhol
    )
    
    # Calculate overall match score with weights
    weights = {
        'text_similarity': 0.35,
        'skill_match': 0.35,
        'education_match': 0.1,
        'english_match': 0.1,
        'spanish_match': 0.1
    }
    
    scores = {
        'text_similarity': text_similarity,
        'skill_match': skill_match,
        'education_match': education_match,
        'english_match': english_match,
        'spanish_match': spanish_match
    }
    
    overall_score = sum(score * weights[category] for category, score in scores.items())
    scores['overall_score'] = overall_score
    
    return scores

def find_matching_candidates(vagas_df: pd.DataFrame, applicants_df: pd.DataFrame, vaga_id: str, 
                            top_n: int = 10) -> pd.DataFrame:
    """
    Find the top N candidates matching a specific job.
    
    Args:
        vagas_df: DataFrame with job vacancies
        applicants_df: DataFrame with applicant data
        vaga_id: ID of the job vacancy to match against
        top_n: Number of top candidates to return
    
    Returns:
        DataFrame with top matching candidates and their scores
    """
    # Get job data
    job_data = vagas_df[vagas_df['vaga_id'] == vaga_id]
    if job_data.empty:
        return pd.DataFrame()
    
    job_series = job_data.iloc[0]
    
    # Calculate similarity for each candidate
    results = []
    
    # Use a subset of candidates for better performance if the dataset is large
    candidates_sample = applicants_df if len(applicants_df) < 1000 else applicants_df.sample(1000)
    
    for index, candidate in candidates_sample.iterrows():
        candidate_dict = {}
        # Convertendo pandas.Series para dict para evitar erros do tipo
        if hasattr(candidate, 'to_dict'):
            candidate_dict = candidate.to_dict()
        else:
            for col in applicants_df.columns:
                candidate_dict[col] = candidate.get(col, '')
                
        similarity_scores = calculate_similarity(job_series, candidate)
        
        result = {
            'codigo': candidate_dict.get('codigo_profissional', ''),
            'nome': candidate_dict.get('nome', ''),
            'area_atuacao': candidate_dict.get('area_atuacao', ''),
            'nivel_academico': candidate_dict.get('nivel_academic', ''),
            'nivel_ingles': candidate_dict.get('nivel_ingles', ''),
            'nivel_espanhol': candidate_dict.get('nivel_espanhol', ''),
            'overall_score': similarity_scores['overall_score'],
            'text_similarity': similarity_scores['text_similarity'],
            'skill_match': similarity_scores['skill_match'],
            'education_match': similarity_scores['education_match'],
            'english_match': similarity_scores['english_match'],
            'spanish_match': similarity_scores['spanish_match']
        }
        results.append(result)
    
    # Create DataFrame and sort by overall score
    results_df = pd.DataFrame(results) if results else pd.DataFrame()
    
    if not results_df.empty:
        results_df = results_df.sort_values('overall_score', ascending=False)
        if top_n > 0:
            results_df = results_df.head(top_n)
    
    return results_df

def get_candidates_by_vaga(vagas_df: pd.DataFrame, prospects_df: pd.DataFrame, applicants_df: pd.DataFrame, 
                          vaga_id: str, include_scores: bool = True) -> pd.DataFrame:
    """
    Get all candidates who have applied for a specific job vacancy with similarity scores.
    
    Args:
        vagas_df: DataFrame with job vacancies
        prospects_df: DataFrame with prospect data
        applicants_df: DataFrame with applicant data
        vaga_id: ID of the job vacancy to get candidates for
        include_scores: Whether to include similarity scores
    
    Returns:
        DataFrame with candidates and their information
    """
    # Get job data
    job_data = vagas_df[vagas_df['vaga_id'] == vaga_id]
    if job_data.empty:
        return pd.DataFrame()
    
    job_series = job_data.iloc[0]
    
    # Get prospects for this job
    job_prospects = prospects_df[prospects_df['vaga_id'] == vaga_id]
    
    if job_prospects.empty:
        return pd.DataFrame()
    
    # Get candidate codes and convert to list (avoiding .unique() on series)
    # This é uma alternativa ao .unique() para evitar erros de tipo
    prospect_codes = list(set(job_prospects['codigo'].tolist()))
    
    # Get candidate information
    results = []
    for code in prospect_codes:
        # Find candidate in applicants data
        candidate_data = applicants_df[applicants_df['codigo_profissional'] == code]
        if candidate_data.empty:
            # If candidate not found in applicants data, use prospect data
            prospect_matches = job_prospects[job_prospects['codigo'] == code]
            if prospect_matches.empty:
                continue
                
            prospect_data = prospect_matches.iloc[0]
            prospect_dict = prospect_data.to_dict() if hasattr(prospect_data, 'to_dict') else {}
                
            candidate = {
                'codigo': code,
                'nome': prospect_dict.get('nome', ''),
                'area_atuacao': '',
                'situacao': prospect_dict.get('situacao_candidado', ''),
                'data_candidatura': prospect_dict.get('data_candidatura', ''),
                'recrutador': prospect_dict.get('recrutador', '')
            }
            
            if include_scores:
                candidate.update({
                    'overall_score': 0,
                    'text_similarity': 0,
                    'skill_match': 0,
                    'education_match': 0,
                    'english_match': 0,
                    'spanish_match': 0
                })
        else:
            # Use applicant data
            candidate_series = candidate_data.iloc[0]
            prospect_matches = job_prospects[job_prospects['codigo'] == code]
            if prospect_matches.empty:
                continue
                
            prospect_data = prospect_matches.iloc[0]
            candidate_dict = candidate_series.to_dict() if hasattr(candidate_series, 'to_dict') else {}
            prospect_dict = prospect_data.to_dict() if hasattr(prospect_data, 'to_dict') else {}
            
            candidate = {
                'codigo': code,
                'nome': candidate_dict.get('nome', ''),
                'area_atuacao': candidate_dict.get('area_atuacao', ''),
                'nivel_academico': candidate_dict.get('nivel_academic', ''),
                'nivel_ingles': candidate_dict.get('nivel_ingles', ''),
                'nivel_espanhol': candidate_dict.get('nivel_espanhol', ''),
                'situacao': prospect_dict.get('situacao_candidado', ''),
                'data_candidatura': prospect_dict.get('data_candidatura', ''),
                'recrutador': prospect_dict.get('recrutador', '')
            }
            
            if include_scores:
                # Calculate similarity scores
                similarity_scores = calculate_similarity(job_series, candidate_series)
                candidate.update({
                    'overall_score': similarity_scores['overall_score'],
                    'text_similarity': similarity_scores['text_similarity'],
                    'skill_match': similarity_scores['skill_match'],
                    'education_match': similarity_scores['education_match'],
                    'english_match': similarity_scores['english_match'],
                    'spanish_match': similarity_scores['spanish_match']
                })
        
        results.append(candidate)
    
    # Create DataFrame and sort by status and score if scores included
    results_df = pd.DataFrame(results) if results else pd.DataFrame()
    
    if not results_df.empty:
        if include_scores and 'overall_score' in results_df.columns:
            results_df = results_df.sort_values(['situacao', 'overall_score'], ascending=[True, False])
    
    return results_df
