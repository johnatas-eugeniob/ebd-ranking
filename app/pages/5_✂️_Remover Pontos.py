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

#credentials = pygsheets.authorize(service_file=os.getcwd() + "./cred.json") # sem deploy
credentials = pygsheets.authorize(service_file=os.getcwd() + "/cred.json") #para deploy

# Inicializa as listas no session_state se não existirem
if 'atividade_selecionada' not in st.session_state:
    st.session_state.atividade_selecionada = []
if 'aluno_selected' not in st.session_state:
    st.session_state.aluno_selected = []

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
        optionP1 = st.checkbox(label="Alex")
        optionP2 = st.checkbox(label="Any")
        optionP3 = st.checkbox(label="Felipe")
        optionP4 = st.checkbox(label="Gabrielly")
        optionP5 = st.checkbox(label="Isaac")
    with op2:
        optionP6 = st.checkbox(label="Isabelle")
        optionP7 = st.checkbox(label="Isabely")
        optionP8 = st.checkbox(label="Jhonny ")
        optionP9 = st.checkbox(label="Mônica")
        optionP10 = st.checkbox(label="Nicole")
    with op3:
        optionP11 = st.checkbox(label="Raissa")
        optionP12 = st.checkbox(label="Rayane")
        optionP13 = st.checkbox(label="Samuel")
    
    aluno_selected = []
    if optionP1:
        aluno_selected.append('Alex')
    if optionP2:
        aluno_selected.append('Any')
    if optionP3:
        aluno_selected.append('Felipe')
    if optionP4:
        aluno_selected.append('Gabrielly')
    if optionP5:
        aluno_selected.append('Isaac')
    if optionP6:
        aluno_selected.append('Isabelle')
    if optionP7:
        aluno_selected.append('Isabely')
    if optionP8:
        aluno_selected.append('Jhonny')
    if optionP9:
        aluno_selected.append('Mônica')
    if optionP10:
        aluno_selected.append('Nicole')
    if optionP11:
        aluno_selected.append('Raissa')
    if optionP12:
        aluno_selected.append('Rayane')
    if optionP13:
        aluno_selected.append('Samuel')
    
    # Armazenando os alunos selecionados no session_state
    st.session_state.aluno_selected = aluno_selected

def sistemaMonetario():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("atividades")
    dataAtv = abaAtv.get_all_values()
    st.title("Atribuição de pontos ")

    # Definir variaveis
    taxa_conversao = 3600

    # Iterar pelas linhas (começando da segunda linha para ignorar o cabeçalho, se existir)
    for i in range(1, len(dataAtv)):  # Assume que a primeira linha (índice 0) é o cabeçalho
        try:
            valor_coluna_27 = int(dataAtv[i][26]) # Acessa a coluna 27 (índice 26) e converte para inteiro
        except ValueError:
            print(f"Erro na linha {i+1}: valor na coluna 27 não é um número válido.")
            continue # Pula para a próxima iteração se houver erro de conversão

        if valor_coluna_27 > taxa_conversao:
            diferenca = valor_coluna_27 - taxa_conversao

            try:
                dataAtv[i][25] = int(dataAtv[i][25]) + 1 # Incrementa a coluna 26 (índice 25)
            except ValueError:
                dataAtv[i][25] = 1 # Define para 1 caso não seja um número (ex: célula vazia ou texto)
                print(f"Aviso na linha {i+1}: valor na coluna 26 não era um número, foi definido para 1")

            dataAtv[i][26] = diferenca  # Atualiza a coluna 27 com a diferença

    # Atualizar a planilha com os novos valores
    abaAtv.update('A1', dataAtv) #Atualiza toda a planilha com os dados modificados

    st.success("Planilha atualizada com sucesso!")

def tirarPontos(sub_points):
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("atividades")
    dataAtv = abaAtv.get_all_values()
    if (
            "atividade_selecionada" in st.session_state and 
            st.session_state.atividade_selecionada and 
            "aluno_selected" in st.session_state and 
            st.session_state.aluno_selected
        ):
            atividade_selecionada = st.session_state.atividade_selecionada
            aluno_selected = st.session_state.aluno_selected

            # Localizar a coluna da atividade selecionada
            coluna_atividade = dataAtv[0].index(atividade_selecionada)  # Assumindo que a primeira linha tenha os títulos das atividades

            # Para cada aluno selecionado, encontrar a linha correspondente e inserir os pontos
            for aluno in aluno_selected:
                # Localizar a linha do aluno na planilha
                for i, row in enumerate(dataAtv[1:], start=2):  # A primeira linha é a de cabeçalhos, então começamos do índice 2
                    if row[0] == aluno:  # Supondo que os nomes dos alunos estão na primeira coluna
                    # Atualiza a célula com os pontos
                        # Obter o valor atual na célula
                        valor_atual = abaAtv.cell((i, coluna_atividade + 1)).value  # +1 porque pygsheets usa 1-based index
                        
                        # Tratar valor vazio como zero
                        valor_atual = int(valor_atual) if valor_atual else 0
                        
                        # Somar os pontos
                        novo_valor = valor_atual - sub_points
                        # Antes verificar o valor contido na célula e somar com a variavel sub_points
                        # se o valor na célula for vazio entenda como 0
                        abaAtv.update_value((i, coluna_atividade + 1), novo_valor)  # +1 porque pygsheets usa 1-based index

            st.success(f"Ponto(s) subtraido(s) com sucesso do(s) aluno(s): {', '.join(aluno_selected)}!")
            st.write(f"Atividade selecionada: {st.session_state.atividade_selecionada}. ")
            st.write(f"Pontos a serem subtraidos: {sub_points}")
    else:
        st.error("Variáveis vazias! Preencha todas as informações.")

with st.container(border=True):
    st.title("Remoção de pontos 🎯")
    with st.form(key="Remover pontuação"):
        dropAtividades()
        listNames()
        st.write("___")

        sub_points = st.number_input(label="Quantos ciclos serão removidos?")
        sub_button = st.form_submit_button("Remover Pontos")
        if sub_button:
            tirarPontos(sub_points)

    # Atualizar a tabela de alunos
        # Verificar se a função deve ser recarregada
        if "reload_aba" not in st.session_state:
            st.session_state.reload_aba = False

        # Carregar a aba inicialmente ou quando o estado indicar recarga
        if not st.session_state.reload_aba:
            abaAtividades()
        #Botão para atualizar a tabela    
        att_table = st.form_submit_button("Atualizar tabela")
        if att_table:
            # Atualizar o estado para recarregar a aba
            st.session_state.reload_aba = True
            sistemaMonetario() # Chama a função para atualizar as
            st.rerun()  # Recarregar a página para executar novamente a função