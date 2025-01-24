import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets
import os

st.set_page_config(page_title="Aréa Livre", 
                   page_icon="♾️", 
                   layout="wide"                   
                )
#st.set_page_config(page_icon = './task_icon.png')

credentials = pygsheets.authorize(service_file=os.getcwd() + "./cred.json") # sem deploy
#credentials = pygsheets.authorize(service_file=os.getcwd() + "/cred.json") #para deploy

def sidebar():
    with st.sidebar:
      st.warning("Atenção!\nNão altere os campos de 'TOTAL' (geralmente a última ou as duas últimas colunas de cada planilha), pois as mesmas possuem fórmulas que não podem ser deletadas.")
    
def matrizAtividades():
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

   #st.dataframe(dfAtv)

   # Configurando o Ag-Grid
   gb = GridOptionsBuilder.from_dataframe(dfAtv)
   gb.configure_pagination(enabled=True)  # Habilitar paginação
   gb.configure_side_bar()  # Barra lateral para configurações extras
   gb.configure_default_column(editable=True)  # Permitir edição de todas as células
   grid_options = gb.build()

   # Exibindo a planilha editável
   grid_response = AgGrid(
      dfAtv,
      gridOptions=grid_options,
      update_mode=GridUpdateMode.VALUE_CHANGED,  # Detecta alterações ao editar
      fit_columns_on_grid_load=True,
      theme="streamlit"  # Tema da planilha
   )

   # Capturando o DataFrame atualizado
   df_updated = grid_response["data"]

   #st.write("Dados atualizados:")
   #st.dataframe(pd.DataFrame(df_updated), width=1200)
   # Botão para enviar as alterações ao Google Sheets

   if st.form_submit_button("Salvar alterações na planilha"):
      # Atualizando os dados no Google Sheets
      abaAtv.clear()  # Limpa os dados antigos
      abaAtv.set_dataframe(df_updated, (1, 1))  # Atualiza a planilha com os novos dados
      st.success("Alterações salvas com sucesso no Google Sheets!")

def matrizFichario():
   meuArquivoGsheetsAtv = "https://docs.google.com/spreadsheets/d/1CKUx4qySqsdmqhp_Xv0A9_BewcC9ekmm2Q1eiro1a_U/edit?usp=sharing"
   arquivo = credentials.open_by_url(meuArquivoGsheetsAtv)
   abaAtv = arquivo.worksheet_by_title("fichario")
   dataFc = abaAtv.get_all_values()
   
   # Criando DataFrame corretamente
   dfFc = pd.DataFrame(dataFc[1:], columns=dataFc[0])

   # Convertendo nomes das colunas para strings
   dfFc.columns = dfFc.columns.map(str)
   
   # Removendo espaços extras dos nomes das colunas
   dfFc.columns = dfFc.columns.str.strip()

   # Limpando colunas vazias
   dfFc.columns = [col if col != '' else f"Unnamed_{i}" for i, col in enumerate(dfFc.columns)]
   
   # Removendo colunas duplicadas
   dfFc = dfFc.loc[:, ~dfFc.columns.duplicated(keep='first')]

   #st.dataframe(dfFc) # Só até aqui exibe como planilha porém sem edição

   # Configurando o Ag-Grid
   gb = GridOptionsBuilder.from_dataframe(dfFc)
   gb.configure_pagination(enabled=True)  # Habilitar paginação
   gb.configure_side_bar()  # Barra lateral para configurações extras
   gb.configure_default_column(editable=True)  # Permitir edição de todas as células
   grid_options = gb.build()

   # Exibindo a planilha editável
   grid_response = AgGrid(
      dfFc,
      gridOptions=grid_options,
      update_mode=GridUpdateMode.VALUE_CHANGED,  # Detecta alterações ao editar
      fit_columns_on_grid_load=True,
      theme="streamlit"  # Tema da planilha
   )

   # Capturando o DataFrame atualizado
   df_updated = grid_response["data"]

   #st.write("Dados atualizados:")
   #st.dataframe(pd.DataFrame(df_updated), width=1200)

   if st.form_submit_button("Salvar alterações na planilha"):
      # Atualizando os dados no Google Sheets
      abaAtv.clear()  # Limpa os dados antigos
      abaAtv.set_dataframe(df_updated, (1, 1))  # Atualiza a planilha com os novos dados
      st.success("Alterações salvas com sucesso no Google Sheets!")

# Principal
sidebar()
with st.container(border=True):
   st.title("Matrizes de Edição Livre ♾️")
   st.warning("Leia com atenção a mensagem ao lado")

   with st.form(key="attAtividades"):
      st.subheader("Matriz de Atividades")
      matrizAtividades()

   st.write("___")

   with st.form(key="attFichario"):
      st.subheader("Matriz de Fichario")
      matrizFichario()
