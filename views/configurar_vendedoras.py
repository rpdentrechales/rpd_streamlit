import streamlit as st
import pandas as pd
import datetime
from auxiliar.auxiliar import *

st.set_page_config(page_title="RPD - Configurar Vendedoras", page_icon="💎",layout="wide")

st.title("Testes - Link das vendedoras")

vendedoras_df = get_dataframe_from_mongodb(collection_name="dados_vendedoras", database_name="rpd_db")

nome_das_vendedoras = sorted(vendedoras_df["nome_vendedora"].unique())

vendedora_selecionada = st.selectbox("Selecione uma Vendedora", nome_das_vendedoras)

id_vendedora = vendedoras_df.loc[vendedoras_df["nome_vendedora"] == vendedora_selecionada, "id_vendedora"].values[0]

st.markdown(f'[Abrir site da vendedora](https://rpd-visualizar.streamlit.app//visualisar?id={id_vendedora})')
