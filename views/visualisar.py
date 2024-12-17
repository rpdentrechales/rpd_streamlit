import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from auxiliar.auxiliar import *
import plotly.express as px

st.set_page_config(page_title="Pró-Corpo - Visualizar Vendas", page_icon="💎",layout="wide")

url_parameters = st.query_params
error_page = True

if "id" in url_parameters:

  id_vendedora = st.query_params["id"]
  vendedoras_df = get_dataframe_from_mongodb(collection_name="dados_vendedoras", database_name="rpd_db")
  vendedoras_df = vendedoras_df.loc[vendedoras_df["id_vendedora"] == id_vendedora]
  nome_vendedora = vendedoras_df["nome_vendedora"].iloc[0]

  if nome_vendedora:
    query = {"created_by": nome_vendedora}

    billcharges_vendedoras_df = get_dataframe_from_mongodb(collection_name="billcharges_db", database_name="dash_midia",query=query)
    st.title("Visualizar Vendas")
    st.write(f"Olá, {nome_vendedora}")
    
    billcharges_vendedoras_df["due_at"] = pd.to_datetime(billcharges_vendedoras_df['due_at'], format="%Y-%m-%d %H:%M:%S").dt.strftime("%Y-%m-%d")
    billcharges_vendedoras_df['due_at'] = pd.to_datetime(billcharges_vendedoras_df['due_at'])
    billcharges_vendedoras_df['date'] = pd.to_datetime(billcharges_vendedoras_df['date'])
    billcharges_vendedoras_df['avista'] = billcharges_vendedoras_df.apply(lambda row: row['amount'] if row['due_at'] == row['date'] else 0, axis=1)

    groupby_quote = billcharges_vendedoras_df.groupby(['quote_id','customer_id']).agg({'amount': 'sum', 'avista': 'sum'}).reset_index()
    
    st.dataframe(groupby_quote)

    error_page = False

if error_page:
  st.title("Página não encontrada")
