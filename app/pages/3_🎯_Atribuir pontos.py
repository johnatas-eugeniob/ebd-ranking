import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets
import os
from datetime import datetime, timedelta
from gspread_formatting import *
from gspread_formatting import color

st.set_page_config(page_title="PONTUAÇÃO", 
                   page_icon="🎯", 
                   layout="wide"                   
                )
#st.set_page_config(page_icon = './task_icon.png')

credentials = pygsheets.authorize(service_file=os.getcwd() + "./cred.json")

# Inicializa as listas no session_state se não existirem
if 'atividade_selecionada' not in st.session_state:
    st.session_state.atividade_selecionada = []
if 'aluno_selected' not in st.session_state:
    st.session_state.aluno_selected = []
if 'soma_points' not in st.session_state:
    st.session_state.soma_points = []

def abaAtividades():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("atividades")
    dataAtv = abaAtv.get_all_values()
    
    # Criando DataFrame corretamente
    dfAtv = pd.DataFrame(dataAtv[1:], columns=dataAtv[0])

    # Convertendo nomes das colunas para strings
    dfAtv.columns = dfAtv.columns.map(str)
    
    # Removendo espaços extras dos nomes das colunas
    dfAtv.columns = dfAtv.columns.str.strip()

    # Limpando colunas vazias
    dfAtv.columns = [col if col != '' else f"Unnamed_{i}" for i, col in enumerate(dfAtv.columns)]
    
    # Removendo colunas duplicadas
    dfAtv = dfAtv.loc[:, ~dfAtv.columns.duplicated(keep='first')]

    st.dataframe(dfAtv)

def dropAtividades():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"  
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("atividades")
    dataAtv = abaAtv.get_all_values()

    # Criando DataFrame corretamente, excluindo a primeira linha (usada como dropdown)
    dfAtv = pd.DataFrame(dataAtv[1:], columns=dataAtv[0])

    # Convertendo nomes das colunas para strings e limpando espaços extras
    dfAtv.columns = dfAtv.columns.map(str).str.strip()

    # Obter atividades da primeira linha (horizontalmente)
    atividades = dataAtv[0][1:]  # Ignora a primeira coluna e pega os títulos restantes

    # Criar dropdown para selecionar uma atividade
    atividade_selecionada = st.selectbox("Lista de Atividades:", atividades)

    # Salvar a atividade selecionada no session_state
    st.session_state.atividade_selecionada = atividade_selecionada

    # Filtrar o DataFrame baseado na atividade selecionada
    df_filtrado = dfAtv[['-', atividade_selecionada]]

def listNames():
    st.write("Selecione o(s) aluno(s)")
    op1, op2, op3, op4 = st.columns(4)
    with op1:
        optionP1 = st.checkbox(label="pessoa1")
        optionP2 = st.checkbox(label="pessoa2")
        optionP3 = st.checkbox(label="pessoa3")
        optionP4 = st.checkbox(label="pessoa4")
        optionP5 = st.checkbox(label="pessoa5")
    with op2:
        optionP6 = st.checkbox(label="pessoa6")
        optionP7 = st.checkbox(label="pessoa7")
        optionP8 = st.checkbox(label="pessoa8")
        optionP9 = st.checkbox(label="pessoa9")
        optionP10 = st.checkbox(label="pessoa10")
    with op3:
        optionP11 = st.checkbox(label="pessoa11")
        optionP12 = st.checkbox(label="pessoa12")
        optionP13 = st.checkbox(label="pessoa13")
        optionP14 = st.checkbox(label="pessoa14")
        optionP15 = st.checkbox(label="pessoa15")
    with op4:
        optionP16 = st.checkbox(label="pessoa16")
        optionP17 = st.checkbox(label="pessoa17")
        optionP18 = st.checkbox(label="pessoa18")
        optionP19 = st.checkbox(label="pessoa19")
        optionP20 = st.checkbox(label="pessoa20")
    
    aluno_selected = []
    if optionP1:
        aluno_selected.append('pessoa1')
    if optionP2:
        aluno_selected.append('pessoa2')
    if optionP3:
        aluno_selected.append('pessoa3')
    if optionP4:
        aluno_selected.append('pessoa4')
    if optionP5:
        aluno_selected.append('pessoa5')
    if optionP6:
        aluno_selected.append('pessoa6')
    if optionP7:
        aluno_selected.append('pessoa7')
    if optionP8:
        aluno_selected.append('pessoa8')
    if optionP9:
        aluno_selected.append('pessoa9')
    if optionP10:
        aluno_selected.append('pessoa10')
    
    # Armazenando os alunos selecionados no session_state
    st.session_state.aluno_selected = aluno_selected

def pontosParaReceber():
    st.write("Selecione a area de pontos")
    op1, op2 = st.columns(2)
    with op1:
        optionT1 = st.checkbox(label="1° Lugar no Kahoot (10p)")
        optionT2 = st.checkbox(label="2° Lugar no Kahoot (7p)")
        optionT3 = st.checkbox(label="3° Lugar no Kahoot (5p)")
        optionT4 = st.checkbox(label="Respondeu a dinâmica (5p)")
        optionT5 = st.checkbox(label="Respondeu pergunta direta (5p)")
    with op2:
        optionT6 = st.checkbox(label="Presença (1p)")
        optionT7 = st.checkbox(label="Visitante (10p)")
        optionT8 = st.checkbox(label="Biblia (1p)")
        optionT9 = st.checkbox(label="Revista (1p)")
        #optionT10 = st.checkbox(label="pessoa10")
    
    point_selected = []
    if optionT1:
        point_selected.append(10)
    if optionT2:
        point_selected.append(7)
    if optionT3:
        point_selected.append(5)
    if optionT4:
        point_selected.append(5)
    if optionT5:
        point_selected.append(5)
    if optionT6:
        point_selected.append(1)
    if optionT7:
        point_selected.append(10)
    if optionT8:
        point_selected.append(1)
    if optionT9:
        point_selected.append(1)
    #if optionT10:
        #point_selected.append('pessoa10')

    soma_points = sum(point_selected)
    # Armazenando os alunos selecionados no session_state
    st.session_state.soma_points = soma_points

with st.container(border=True):
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("atividades")
    dataAtv = abaAtv.get_all_values()
    st.title("Atribuição de pontos 🎯")
    with st.form(key="atribuir pontuação"):
        dropAtividades()
        listNames()
        st.write("___")
        pontosParaReceber() 
        submit_button = st.form_submit_button("Enviar")

        if submit_button:
            if (
                "atividade_selecionada" in st.session_state and 
                st.session_state.atividade_selecionada and 
                "aluno_selected" in st.session_state and 
                st.session_state.aluno_selected and 
                "soma_points" in st.session_state and 
                st.session_state.soma_points
            ):
                atividade_selecionada = st.session_state.atividade_selecionada
                aluno_selected = st.session_state.aluno_selected
                soma_points = st.session_state.soma_points

                # Localizar a coluna da atividade selecionada
                coluna_atividade = dataAtv[0].index(atividade_selecionada)  # Assumindo que a primeira linha tenha os títulos das atividades

                # Para cada aluno selecionado, encontrar a linha correspondente e inserir os pontos
                for aluno in aluno_selected:
                    # Localizar a linha do aluno na planilha
                    for i, row in enumerate(dataAtv[1:], start=2):  # A primeira linha é a de cabeçalhos, então começamos do índice 2
                        if row[0] == aluno:  # Supondo que os nomes dos alunos estão na primeira coluna
                            # Atualiza a célula com os pontos
                            abaAtv.update_value((i, coluna_atividade + 1), soma_points)  # +1 porque pygsheets usa 1-based index

                st.success(f"Pontos atribuídos com sucesso aos alunos: {', '.join(aluno_selected)}!")
                st.write(f"Atividade selecionada: {st.session_state.atividade_selecionada}, ")
                st.write(f"Pontos a serem inseridos: {st.session_state.soma_points}")
            else:
                st.error("Variáveis vazias! Preencha todas as informações.")

