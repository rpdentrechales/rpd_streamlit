import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from auxiliar.auxiliar import *
import plotly.express as px

st.set_page_config(page_title="Pró-Corpo - Visualizar Vendas", page_icon="💎",layout="wide")

st.title("Visualizar Vendas")

url_parameters = st.query_params
error_page = True

if "id" in url_parameters:

  id_vendedora = st.query_params["id"]
  vendedoras_df = get_dataframe_from_mongodb(collection_name="dados_vendedoras", database_name="rpd_db")
  vendedoras_df = vendedoras_df.loc[vendedoras_df["id_vendedora"] == id_vendedora]
  nome_vendedora = vendedoras_df["nome_vendedora"].iloc[0]

  if nome_vendedora:
    query = {"nome_vendedora": nome_vendedora}

    billcharges_vendedoras_df = get_dataframe_from_mongodb(collection_name="billcharges_db", database_name="dash_midia",query=query)
    st.tittle(f"Vendas da Vendedora: {nome_vendedora}") 
    st.dataframe(billcharges_vendedoras_df)

    error_page = False

if error_page:
  st.tittle("Página não encontrada")
