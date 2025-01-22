import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets
import os
from datetime import datetime, timedelta
from gspread_formatting import *
from gspread_formatting import color

st.set_page_config(page_title="ATIVIDADES", 
                   page_icon="📄", 
                   layout="wide"                   
                )
#st.set_page_config(page_icon = './task_icon.png')

credentials = pygsheets.authorize(service_file=os.getcwd() + "./cred.json")

# Aba de atividades sendo carregada
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

#dropdown com as atividades
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

    # Filtrar o DataFrame baseado na atividade selecionada
    #df_filtrado = dfAtv[['-', atividade_selecionada]]

# Form para lançamento de atividade
def formsAddLesson():
    # Criando o formulário
    with st.form(key="cadastro_atividade"): 
        st.write("Selecione um professor")
        op1, op2 = st.columns(2)
        with op1:
            optionP1 = st.checkbox(label="Felipe")
            optionP2 = st.checkbox(label="Johnatas")
        with op2:
            optionP3 = st.checkbox(label="Rayane")
            optionP4 = st.checkbox(label="Isaac")
        
        # Lista para armazenar os nomes dos professores
        nome_prof = []
        if optionP1:
            nome_prof.append('Felipe')
        if optionP2:
            nome_prof.append('Johnatas')
        if optionP3:
            nome_prof.append('Rayane')
        if optionP4:
            nome_prof.append('Isaac')

        ft_nome_prof = ", ".join(nome_prof)

        st.write("___")

        atividade = st.text_input("Nome da atividade")

        st.write("___")

        # Definir limites de data
        data_min = datetime.today().date() - timedelta(days=365)  # 1 ano atrás
        data_max = datetime.today().date() + timedelta(days=365)  # 1 ano à frente

        # Entrada de data com limites
        data = st.date_input("Data de lançamento", value=datetime.today().date(), min_value=data_min, max_value=data_max)

        # Formatar a data para o padrão brasileiro (dd/mm/aaaa)
        data_formatada = data.strftime("%d/%m/%Y")
        
        st.write("Data selecionada:", data_formatada)

        submit_button = st.form_submit_button("Enviar")

    # Verificando se o botão foi pressionado
    if submit_button:
        if ft_nome_prof and atividade:
            st.write(f"Prefessor, {ft_nome_prof}.")
            st.write("**Nome da atividade:**", atividade)
            st.write("**Data:**", data_formatada)
            #mandar infos para a planilha
            aplicarFormsContent(ft_nome_prof, atividade, data_formatada)
        else:
            st.error("Por favor, preencha todos os campos obrigatórios e aceite os termos.")

#Aplica o conteudo do forms na planilha
def aplicarFormsContent(ft_nome_prof, atividade, data_formatada):
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("atividades")
    dataAtv = abaAtv.get_all_values(include_tailing_empty=False)

    # Verifica qual é a última coluna preenchida (tamanho da primeira linha)
    ultima_coluna_index = len(dataAtv[0])  # Conta colunas com dados
    nova_coluna_index = ultima_coluna_index + 1  # Define o índice da nova coluna

    # Define o nome da nova coluna
    nova_coluna_nome = f"{ft_nome_prof} - {atividade} - {data_formatada}"

    # Insere o nome da nova coluna no cabeçalho (linha 1)
    abaAtv.update_value((1, nova_coluna_index), nova_coluna_nome)

    # Escreve "pontuação" na célula abaixo da nova coluna (linha 2)
    abaAtv.update_value((2, nova_coluna_index), "pontuação")
    
    st.success(f"Nova coluna, criada com sucesso!")

with st.container(border = True):
    st.title("ATIVIDADES, INTERAÇÕES, DINÂMICAS 📄")
    with st.container(border = True):
        st.subheader("Adcionar atividade")
        formsAddLesson()
        st.write("___")
        st.subheader("Atividades Lançadas")
        dropAtividades()
        abaAtividades()
        