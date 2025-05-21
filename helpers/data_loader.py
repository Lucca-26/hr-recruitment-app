import pandas as pd
import json
import os
import numpy as np
import streamlit as st
from typing import Tuple, Dict, List, Any

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load job vacancy, prospects, and applicants data from files.
    
    Returns:
        Tuple containing three DataFrames:
        - vagas_df: DataFrame with job vacancies
        - prospects_df: DataFrame with prospect data
        - applicants_df: DataFrame with applicant data
    """
    # Define file paths (adjust as needed)
    vagas_path = 'attached_assets/vagas.json'
    prospects_path = 'attached_assets/prospects (1).json'
    applicants_path = 'attached_assets/applicants (1).csv'
    
    # Load vagas.json (job vacancies)
    with open(vagas_path, 'r', encoding='utf-8') as file:
        vagas_json = json.load(file)
    
    # Process vagas data into a flat DataFrame
    vagas_records = []
    for vaga_id, vaga_data in vagas_json.items():
        if 'informacoes_basicas' in vaga_data and 'perfil_vaga' in vaga_data:
            vaga_record = {
                'vaga_id': vaga_id,
                'titulo_vaga': vaga_data['informacoes_basicas'].get('titulo_vaga', ''),
                'cliente': vaga_data['informacoes_basicas'].get('cliente', ''),
                'tipo_contratacao': vaga_data['informacoes_basicas'].get('tipo_contratacao', ''),
                'nivel_profissional': vaga_data['perfil_vaga'].get('nivel profissional', ''),
                'nivel_academico': vaga_data['perfil_vaga'].get('nivel_academico', ''),
                'nivel_ingles': vaga_data['perfil_vaga'].get('nivel_ingles', ''),
                'nivel_espanhol': vaga_data['perfil_vaga'].get('nivel_espanhol', ''),
                'pais': vaga_data['perfil_vaga'].get('pais', ''),
                'estado': vaga_data['perfil_vaga'].get('estado', ''),
                'cidade': vaga_data['perfil_vaga'].get('cidade', ''),
                'areas_atuacao': vaga_data['perfil_vaga'].get('areas_atuacao', ''),
                'principais_atividades': vaga_data['perfil_vaga'].get('principais_atividades', ''),
                'competencia_tecnicas': vaga_data['perfil_vaga'].get('competencia_tecnicas_e_comportamentais', ''),
                'descricao_completa': f"{vaga_data['perfil_vaga'].get('principais_atividades', '')} {vaga_data['perfil_vaga'].get('competencia_tecnicas_e_comportamentais', '')}"
            }
            vagas_records.append(vaga_record)
    
    vagas_df = pd.DataFrame(vagas_records)
    
    # Load prospects.json
    with open(prospects_path, 'r', encoding='utf-8') as file:
        prospects_json = json.load(file)
    
    # Process prospects data into a flat DataFrame
    prospects_rows = []
    for vaga_id, vaga_info in prospects_json.items():
        titulo = vaga_info.get('titulo', '')
        modalidade = vaga_info.get('modalidade', '')
        prospects_list = vaga_info.get('prospects', [])
        
        for prospect in prospects_list:
            prospect_row = {
                'vaga_id': vaga_id,
                'titulo_vaga': titulo,
                'modalidade': modalidade,
                'nome': prospect.get('nome', ''),
                'codigo': prospect.get('codigo', ''),
                'situacao_candidado': prospect.get('situacao_candidado', ''),
                'data_candidatura': prospect.get('data_candidatura', ''),
                'ultima_atualizacao': prospect.get('ultima_atualizacao', ''),
                'comentario': prospect.get('comentario', ''),
                'recrutador': prospect.get('recrutador', '')
            }
            prospects_rows.append(prospect_row)
    
    prospects_df = pd.DataFrame(prospects_rows)
    
    # Load applicants.csv
    applicants_df = pd.read_csv(applicants_path, encoding='utf-8', index_col=0, low_memory=False)
    
    # Clean up applicants DataFrame to handle potential mixed data types
    applicants_df = applicants_df.fillna('')
    
    # Add computed fields for text similarity
    applicants_df['profile_text'] = applicants_df.apply(
        lambda row: f"{row.get('nome', '')} {row.get('titulo_profissional', '')} {row.get('area_atuacao', '')} "
                   f"{row.get('conhecimentos_tecnicos', '')} {row.get('certificacoes', '')} "
                   f"{row.get('qualificacoes', '')}",
        axis=1
    )
    
    return vagas_df, prospects_df, applicants_df

def get_applicant_by_code(applicants_df: pd.DataFrame, codigo: str) -> pd.Series:
    """
    Find an applicant by their code.
    
    Args:
        applicants_df: DataFrame with applicant data
        codigo: Applicant code to search for
    
    Returns:
        Series containing the applicant data or None if not found
    """
    matches = applicants_df[applicants_df['codigo_profissional'] == codigo]
    if not matches.empty:
        return matches.iloc[0]
    return None

def get_vaga_by_id(vagas_df: pd.DataFrame, vaga_id: str) -> pd.Series:
    """
    Find a job vacancy by its ID.
    
    Args:
        vagas_df: DataFrame with job vacancies
        vaga_id: Job vacancy ID to search for
    
    Returns:
        Series containing the job vacancy data or None if not found
    """
    matches = vagas_df[vagas_df['vaga_id'] == vaga_id]
    if not matches.empty:
        return matches.iloc[0]
    return None

def get_prospects_by_vaga(prospects_df: pd.DataFrame, vaga_id: str) -> pd.DataFrame:
    """
    Find all prospects for a given job vacancy.
    
    Args:
        prospects_df: DataFrame with prospect data
        vaga_id: Job vacancy ID to filter by
    
    Returns:
        DataFrame containing the filtered prospects
    """
    return prospects_df[prospects_df['vaga_id'] == vaga_id]
