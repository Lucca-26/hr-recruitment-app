import pandas as pd
import json
from typing import Tuple

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Carrega os dados de vagas, prospectos e candidatos.
    
    Returns:
        Tuple contendo três DataFrames:
        - vagas_df: DataFrame com vagas
        - prospects_df: DataFrame com prospectos
        - applicants_df: DataFrame com candidatos
    """
    # Carregar dados de vagas
    with open('vagas.json', 'r', encoding='utf-8') as f:
        vagas_data = json.load(f)
    vagas_df = pd.DataFrame(vagas_data)
    
    # Carregar dados de prospectos
    with open('prospects.json', 'r', encoding='utf-8') as f:
        prospects_data = json.load(f)
    prospects_df = pd.DataFrame(prospects_data)
    
    # Carregar dados de candidatos
    applicants_df = pd.read_csv('applicants.csv', encoding='utf-8')
    
    return vagas_df, prospects_df, applicants_df

def get_applicant_by_code(applicants_df: pd.DataFrame, codigo: str) -> pd.Series:
    """
    Encontra um candidato pelo código.
    
    Args:
        applicants_df: DataFrame com dados de candidatos
        codigo: Código do candidato a ser buscado
    
    Returns:
        Series contendo os dados do candidato ou None se não encontrado
    """
    applicant = applicants_df[applicants_df['codigo_profissional'] == codigo]
    if applicant.empty:
        return None
    return applicant.iloc[0]

def get_vaga_by_id(vagas_df: pd.DataFrame, vaga_id: str) -> pd.Series:
    """
    Encontra uma vaga pelo ID.
    
    Args:
        vagas_df: DataFrame com vagas
        vaga_id: ID da vaga a ser buscada
    
    Returns:
        Series contendo os dados da vaga ou None se não encontrada
    """
    vaga = vagas_df[vagas_df['vaga_id'] == vaga_id]
    if vaga.empty:
        return None
    return vaga.iloc[0]

def get_prospects_by_vaga(prospects_df: pd.DataFrame, vaga_id: str) -> pd.DataFrame:
    """
    Encontra todos os prospectos para uma determinada vaga.
    
    Args:
        prospects_df: DataFrame com dados de prospectos
        vaga_id: ID da vaga para filtrar
    
    Returns:
        DataFrame contendo os prospectos filtrados
    """
    return prospects_df[prospects_df['vaga_id'] == vaga_id]