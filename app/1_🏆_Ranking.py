import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets
import os

st.set_page_config(page_title="RANKING EBD", 
                   page_icon="🏆", 
                   layout="wide"                   
                )
#st.set_page_config(page_icon = './task_icon.png')

#credentials = pygsheets.authorize(service_file=os.getcwd() + "./cred.json") # sem deploy
credentials = pygsheets.authorize(service_file=os.getcwd() + "/cred.json") #para deploy

def sidebar():
    with st.sidebar:
        pass

# Aba de atividades sendo carregada
def abaAtividades():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("atividades")
    dataAtv = abaAtv.get_all_values()
    dfAtv = pd.DataFrame(dataAtv)
    dfAtv.iloc[1, 2]

    st.dataframe(dfAtv)

# Aba de Ranking para exibição
def abaRanking():
    meuArquivoGsheetsRk = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsRk)
    abaRk = arquivo.worksheet_by_title("ranking")
    dataRk = abaRk.get_all_values()
    # Usando a primeira linha como cabeçalho e os dados a partir da segunda linha
    dfRk = pd.DataFrame(dataRk[1:], columns=dataRk[0])
    
    # Limpando as colunas com nome duplicado ou vazio
    dfRk.columns = [col if col != '' else f"Unnamed_{i}" for i, col in enumerate(dfRk.columns)]
    
    # Remover colunas duplicadas
    dfRk = dfRk.loc[:, ~dfRk.columns.duplicated()]

    # Certifique-se de que os dados são numéricos para ranking
    dfRk['ranking'] = pd.to_numeric(dfRk['ranking'], errors='coerce')

    # Ordenando pelo ranking (do maior para o menor) e pegando os 3 primeiros
    top3_df = dfRk.sort_values(by='ranking', ascending=True).head(3)

    # Exibindo as métricas no Streamlit
    st.title("Top 3 Alunos 🏆")
    for _, aluno in top3_df.iterrows():
        st.metric(label=f"🏆 {aluno['nome']}", value=f"{aluno['ranking']}° lugar")

def tabela():
    meuArquivoGsheetsRk = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsRk)
    abaRk = arquivo.worksheet_by_title("ranking")
    dataRk = abaRk.get_all_values()
    # Usando a primeira linha como cabeçalho e os dados a partir da segunda linha
    dfRk = pd.DataFrame(dataRk[1:], columns=dataRk[0])
    
    # Limpando as colunas com nome duplicado ou vazio
    dfRk.columns = [col if col != '' else f"Unnamed_{i}" for i, col in enumerate(dfRk.columns)]
    
    # Remover colunas duplicadas
    dfRk = dfRk.loc[:, ~dfRk.columns.duplicated()]

    # Certifique-se de que os dados são numéricos para ranking
    dfRk['ranking'] = pd.to_numeric(dfRk['ranking'], errors='coerce')

    # Ordenando pelo ranking (do maior para o menor) e pegando os 3 primeiros
    top3_df = dfRk.sort_values(by='ranking', ascending=False)

    # Exibindo as métricas no Streamlit
    st.title("Tabela completa descrescente")
    for _, aluno in top3_df.iterrows():
        st.metric(label=f"{aluno['nome']}", value=f"{aluno['ranking']}° lugar")

#Container grande na parte superior da pag
with st.container(border = True):
    abaRanking()

with st.container(border=True):
    tabela()

#Colocando uma sidebar na parada
sidebar()