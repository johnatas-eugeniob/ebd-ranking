import streamlit as st
import pandas as pd
import altair as alt
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets
import os

st.set_page_config(page_title="FICHARIO", 
                   page_icon="📒", 
                   layout="wide"                   
                )
#st.set_page_config(page_icon = './task_icon.png')

#credentials = pygsheets.authorize(service_file=os.getcwd() + "./cred.json") # sem deploy
credentials = pygsheets.authorize(service_file=os.getcwd() + "/cred.json") #para deploy

def graficoPresenca():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("fichario")
    dataAtv = abaAtv.get_all_values()

    # Criando DataFrame
    dfAtv = pd.DataFrame(dataAtv[1:], columns=dataAtv[0])

    # Verificando os dados para garantir que as colunas 'nome' e 'presença' estão corretas
    print(dfAtv.head())

    # Garantindo que 'nome' e 'presença' estão no formato adequado
    dfAtv['presença'] = pd.to_numeric(dfAtv['presença'], errors='coerce')

    # Plotando o gráfico de barras
    st.bar_chart(dfAtv.set_index('nome')['presença'])

def graficoVisitantes():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("fichario")
    dataAtv = abaAtv.get_all_values()

    # Criando DataFrame
    dfAtv = pd.DataFrame(dataAtv[1:], columns=dataAtv[0])

    # Verificando os dados para garantir que as colunas 'nome' e 'visitantes' estão corretas
    print(dfAtv.head())

    # Garantindo que 'nome' e 'visitantes' estão no formato adequado
    dfAtv['visitantes'] = pd.to_numeric(dfAtv['visitantes'], errors='coerce')

    # Plotando o gráfico de barras
    st.bar_chart(dfAtv.set_index('nome')['visitantes'])

def graficoBiblia():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("fichario")
    dataAtv = abaAtv.get_all_values()

    # Criando DataFrame
    dfAtv = pd.DataFrame(dataAtv[1:], columns=dataAtv[0])

    # Verificando os dados para garantir que as colunas 'nome' e 'biblia' estão corretas
    print(dfAtv.head())

    # Garantindo que 'nome' e 'biblia' estão no formato adequado
    dfAtv['biblia'] = pd.to_numeric(dfAtv['biblia'], errors='coerce')

    # Plotando o gráfico de barras
    st.bar_chart(dfAtv.set_index('nome')['biblia'])

def graficoRevista():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("fichario")
    dataAtv = abaAtv.get_all_values()

    # Criando DataFrame
    dfAtv = pd.DataFrame(dataAtv[1:], columns=dataAtv[0])

    # Verificando os dados para garantir que as colunas 'nome' e 'revista' estão corretas
    print(dfAtv.head())

    # Garantindo que 'nome' e 'revista' estão no formato adequado
    dfAtv['revista'] = pd.to_numeric(dfAtv['revista'], errors='coerce')

    # Plotando o gráfico de barras
    st.bar_chart(dfAtv.set_index('nome')['revista'])

def participacao():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("fichario")
    dataAtv = abaAtv.get_all_values()

    # Criando DataFrame
    dfAtv = pd.DataFrame(dataAtv[1:], columns=dataAtv[0])

    # Verificando os dados para garantir que as colunas 'nome' e 'participação' estão corretas
    print(dfAtv.head())

    # Garantindo que 'nome' e 'participação' estão no formato adequado
    dfAtv['participação'] = pd.to_numeric(dfAtv['participação'], errors='coerce')

    # Plotando o gráfico de barras
    st.bar_chart(dfAtv.set_index('nome')['participação'])

def oferta():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("fichario")
    dataAtv = abaAtv.get_all_values()

    # Criando DataFrame
    dfAtv = pd.DataFrame(dataAtv[1:], columns=dataAtv[0])

    # Verificando os dados para garantir que as colunas 'nome' e 'oferta' estão corretas
    print(dfAtv.head())

    # Garantindo que 'nome' e 'oferta' estão no formato adequado
    dfAtv['oferta'] = pd.to_numeric(dfAtv['oferta'], errors='coerce')

    # Plotando o gráfico de barras
    st.bar_chart(dfAtv.set_index('nome')['oferta'])
    
def total():
    meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
    arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
    abaAtv = arquivo.worksheet_by_title("fichario")
    dataAtv = abaAtv.get_all_values()

    # Criando DataFrame
    dfAtv = pd.DataFrame(dataAtv[1:], columns=dataAtv[0])

    # Verificando os dados para garantir que as colunas 'nome' e 'total' estão corretas
    print(dfAtv.head())

    # Garantindo que 'nome' e 'total' estão no formato adequado
    dfAtv['total'] = pd.to_numeric(dfAtv['total'], errors='coerce')

    # Plotando o gráfico de barras
    st.bar_chart(dfAtv.set_index('nome')['total'])

with st.container(border=True):
    st.title("FICHARIO 📒")
    st.write("___")
    with st.container(border=True):
        st.subheader("Presença 🙋")
        graficoPresenca()
        st.write("___")
    with st.container(border=True):
        st.subheader("Visitantes ✌️")
        graficoVisitantes()
        st.write("___")
    with st.container(border=True):
        st.subheader("Biblia 📖")
        graficoBiblia()
        st.write("___")
    with st.container(border=True):
        st.subheader("Revista 📔")
        graficoRevista()
        st.write("___")
    with st.container(border=True):
        st.subheader("Participacao 🕺")
        participacao()
        st.write("___")
    with st.container(border=True):
        st.subheader("Oferta 🪙")
        oferta()
        st.write("___")
    with st.container(border=True):
        st.title("Total ♾️")
        total()
        st.write("___")


