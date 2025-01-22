import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets
import os

st.set_page_config(page_title="FICHARIO", 
                   page_icon="📒", 
                   layout="wide"                   
                )
#st.set_page_config(page_icon = './task_icon.png')

credentials = pygsheets.authorize(service_file=os.getcwd() + "./cred.json")

with st.container(border=True):
    st.title("Fichario")
