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
if 'soma_points' not in st.session_state:
    st.session_state.soma_points = []
if 'fichario_points' not in st.session_state:
    st.session_state.fichario_points = []
if 'area_pts_selected' not in st.session_state:
    st.session_state.area_pts_selected = []

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
        optionP8 = st.checkbox(label="Jhonny")
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

def pontosParaReceber():
    st.write("Selecione a area de pontos")
    op1, op2, op3 = st.columns(3)
    with op1:
        optionT1 = st.checkbox(label="Presença (100s)")
        optionT2 = st.checkbox(label="Revista (50s)")
        optionT3 = st.checkbox(label="Biblia (50s)")
        optionT4 = st.checkbox(label="Participação (50s)")
        optionT5 = st.checkbox(label="Visitante (500s)")    
        optionT6 = st.checkbox(label="Oferta (200s)")    
    with op2:
        optionT7 = st.checkbox(label="Respondeu pergunta direta (300s)")
        optionT8 = st.checkbox(label="Resolução de dinâmica (200s)")
        optionT9 = st.checkbox(label="Apresentação Final/Apresentação (1000s)")
        optionT10 = st.checkbox(label="1° Lugar em jogos (500s)")
        optionT11 = st.checkbox(label="2° Lugar em jogos (400s)")
    with op3:
        optionT12 = st.checkbox(label="3° Lugar em jogos (300s)")

    fichario_selected = []
    point_selected = []
    area_pts = []
    if optionT1:
        point_selected.append(100)
        fichario_selected.append(1)
        area_pts.append('presença')
    if optionT2:
        point_selected.append(50)
        fichario_selected.append(1)
        area_pts.append('revista')
    if optionT3:
        point_selected.append(50)
        fichario_selected.append(1)
        area_pts.append('biblia')
    if optionT4:
        point_selected.append(50)
        fichario_selected.append(1)
        area_pts.append('participação')
    if optionT5:
        point_selected.append(500)
        fichario_selected.append(1)
        area_pts.append('visitantes')
    if optionT6:
        point_selected.append(200)
        fichario_selected.append(1)
        area_pts.append('oferta')
    if optionT7:
        point_selected.append(300)
    if optionT8:
        point_selected.append(300)
    if optionT9:
        point_selected.append(1000)
    if optionT10:
        point_selected.append(500)
    if optionT11:
        point_selected.append(400)
    if optionT12:
        point_selected.append(300)

    soma_points = sum(point_selected)
    # Armazenando os alunos selecionados no session_state
    st.session_state.soma_points = soma_points
    st.session_state.fichario_points = fichario_selected
    st.session_state.area_pts_selected = area_pts

def abaFichario():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaFch = arquivo.worksheet_by_title("fichario")
    dataFch = abaFch.get_all_values()
    
    # Criando DataFrame corretamente
    dfFch = pd.DataFrame(dataFch[1:], columns=dataFch[0])

    # Convertendo nomes das colunas para strings
    dfFch.columns = dfFch.columns.map(str)
    
    # Removendo espaços extras dos nomes das colunas
    dfFch.columns = dfFch.columns.str.strip()

    # Limpando colunas vazias
    dfFch.columns = [col if col != '' else f"Unnamed_{i}" for i, col in enumerate(dfFch.columns)]
    
    # Removendo colunas duplicadas
    dfFch = dfFch.loc[:, ~dfFch.columns.duplicated(keep='first')]

    st.dataframe(dfFch)

def atribuirFichario():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaFch = arquivo.worksheet_by_title("fichario")
    dataFch = abaFch.get_all_values()
    
    if (
        "aluno_selected" in st.session_state and 
        st.session_state.aluno_selected and 
        "fichario_points" in st.session_state and
        st.session_state.fichario_points and
        "area_pts_selected" in st.session_state and
        st.session_state.area_pts_selected
    ):
        area_pts_selected = st.session_state.area_pts_selected  # Lista de áreas
        fichario_points = st.session_state.fichario_points  # Lista de pontos para cada área
        aluno_selected = st.session_state.aluno_selected  # Lista de alunos
        
        # Verificar se area_pts_selected é uma lista; se não for, convertê-la para lista
        if not isinstance(area_pts_selected, list):
            area_pts_selected = [area_pts_selected]

        if not isinstance(fichario_points, list):
            fichario_points = [fichario_points] * len(area_pts_selected)  # Repetir o valor se for único
        
        # Garantir que a quantidade de pontos corresponde ao número de áreas selecionadas
        if len(area_pts_selected) != len(fichario_points):
            st.error("A quantidade de áreas e pontos fornecidos não correspondem.")
            return

        # Iterar sobre todas as áreas selecionadas
        for area, pontos in zip(area_pts_selected, fichario_points):
            if area in dataFch[0]:
                coluna_fichario = dataFch[0].index(area)
            else:
                st.error(f"A área selecionada '{area}' não foi encontrada no cabeçalho da planilha.")
                continue  # Pula para a próxima área

            # Para cada aluno selecionado, encontrar a linha correspondente e inserir os pontos
            for aluno in aluno_selected:
                for i, row in enumerate(dataFch[1:], start=2):  
                    if row[0] == aluno:  
                        valor_atual = abaFch.cell((i, coluna_fichario + 1)).value
                                
                        # Tratar valor vazio como zero
                        valor_atual = int(valor_atual) if valor_atual else 0
                        
                        pontos = int(pontos)  # Converter pontos para inteiro
                        novo_valor = valor_atual + pontos

                        # Atualizar o valor na célula correspondente
                        abaFch.update_value((i, coluna_fichario + 1), novo_valor)

        st.success(f"Fichario atualizado com sucesso!")
    else:
        st.error("Variáveis vazias!")

def somarPontos():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("atividades")
    dataAtv = abaAtv.get_all_values()
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
                        # Obter o valor atual na célula
                        valor_atual = abaAtv.cell((i, coluna_atividade + 1)).value  # +1 porque pygsheets usa 1-based index
                        
                        # Tratar valor vazio como zero
                        valor_atual = int(valor_atual) if valor_atual else 0
                        
                        # Somar os pontos
                        novo_valor = valor_atual + soma_points
                        # Antes verificar o valor contido na célula e somar com a variavel soma_points
                        # se o valor na célula for vazio entenda como 0
                        abaAtv.update_value((i, coluna_atividade + 1), novo_valor)  # +1 porque pygsheets usa 1-based index

            st.success(f"Ponto(s) atribuído(s) com sucesso ao(s) aluno(s): {', '.join(aluno_selected)}!")
            st.write(f"Atividade selecionada: {st.session_state.atividade_selecionada}. ")
            st.write(f"Pontos a serem inseridos: {st.session_state.soma_points}")
    else:
        st.error("Variáveis vazias! Preencha todas as informações.")

def sistemaMonetario():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("atividades")
    dataAtv = abaAtv.get_all_values()
    st.title("Atribuição de pontos ")
    pass

with st.container(border=True):
    st.title("Atribuição 🎯")
    with st.form(key="atribuir pontuação"):
        dropAtividades()
        listNames()
        st.write("___")
        pontosParaReceber() 

        submit_button = st.form_submit_button("Enviar")

        if submit_button:
            somarPontos()
            atribuirFichario()

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
            #sistemaMonetario() # Chama a função para atualizar as
            st.rerun()  # Recarregar a página para executar novamente a função