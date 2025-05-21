import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from typing import Tuple, Dict, List, Any
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Carregar modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- Funções auxiliares ---
def preprocess_text(text):
    if pd.isnull(text):
        return ""
    return str(text).lower().strip()

def compute_embedding(text):
    return model.encode([text])[0]

def match_score(text1, text2):
    emb1 = compute_embedding(preprocess_text(text1))
    emb2 = compute_embedding(preprocess_text(text2))
    return cosine_similarity([emb1], [emb2])[0][0]

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    vagas_path = 'vagas.json'
    prospects_path = 'prospects.json'
    applicants_path = 'applicants.csv'

    with open(vagas_path, 'r', encoding='utf-8') as file:
        vagas_json = json.load(file)

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

    with open(prospects_path, 'r', encoding='utf-8') as file:
        prospects_json = json.load(file)

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

    applicants_df = pd.read_csv(applicants_path, encoding='utf-8', index_col=0, low_memory=False)
    applicants_df = applicants_df.fillna('')
    applicants_df['profile_text'] = applicants_df.apply(
        lambda row: f"{row.get('nome', '')} {row.get('titulo_profissional', '')} {row.get('area_atuacao', '')} {row.get('conhecimentos_tecnicos', '')} {row.get('certificacoes', '')} {row.get('qualificacoes', '')}",
        axis=1
    )

    return vagas_df, prospects_df, applicants_df

def get_applicant_by_code(applicants_df: pd.DataFrame, codigo: str) -> pd.Series:
    matches = applicants_df[applicants_df['codigo_profissional'] == codigo]
    if not matches.empty:
        return matches.iloc[0]
    return None

def get_vaga_by_id(vagas_df: pd.DataFrame, vaga_id: str) -> pd.Series:
    matches = vagas_df[vagas_df['vaga_id'] == vaga_id]
    if not matches.empty:
        return matches.iloc[0]
    return None

def get_prospects_by_vaga(prospects_df: pd.DataFrame, vaga_id: str) -> pd.DataFrame:
    return prospects_df[prospects_df['vaga_id'] == vaga_id]
