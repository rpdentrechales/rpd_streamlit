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
    
    billcharges_vendedoras_df["amount"] = billcharges_vendedoras_df["amount"]/10
    billcharges_vendedoras_df["due_at"] = pd.to_datetime(billcharges_vendedoras_df['due_at'], format="%Y-%m-%d %H:%M:%S").dt.strftime("%Y-%m-%d")
    billcharges_vendedoras_df['due_at'] = pd.to_datetime(billcharges_vendedoras_df['due_at'])
    billcharges_vendedoras_df['date'] = pd.to_datetime(billcharges_vendedoras_df['date'])
    billcharges_vendedoras_df['formatted_date'] = billcharges_vendedoras_df['date'].dt.strftime('%d/%m/%Y')
    billcharges_vendedoras_df['period'] = billcharges_vendedoras_df['date'].dt.strftime('%m/%Y')
    billcharges_vendedoras_df['avista'] = billcharges_vendedoras_df.apply(lambda row: row['amount'] if row['due_at'] == row['date'] else 0, axis=1)

    billcharges_vendedoras_df["quote_id"] = billcharges_vendedoras_df["quote_id"].astype(str)
    billcharges_vendedoras_df["customer_id"] = billcharges_vendedoras_df["customer_id"].astype(str)
    
    seletor_mes = st.selectbox("Selecione um mês", billcharges_vendedoras_df["period"].unique())
    billcharges_vendedoras_df = billcharges_vendedoras_df.loc[billcharges_vendedoras_df["period"] == seletor_mes]

    graph_1, graph_2 = st.columns(2)

    with graph_1:
      plot_sales_count(billcharges_vendedoras_df)

    with graph_2:
      plot_total_sales(billcharges_vendedoras_df)

    groupby_quote = billcharges_vendedoras_df.groupby(['quote_id','customer_id']).agg({'amount': 'sum', 'avista': 'sum'}).reset_index()
    
    column_config ={
                   "amount": st.column_config.NumberColumn(
                    "Valor Total",
                    format="R$%d",
                     ),
                    "avista": st.column_config.NumberColumn(
                    "Valor à Vista",
                    format="R$%d",
                    )
                  }

    seletor_dia = st.selectbox("Selecione um dia", billcharges_vendedoras_df["formatted_date"].unique())
    
    resumo_1, resumo_2 = st.columns([3,1])

    billcharges_vendedoras_df_dia = billcharges_vendedoras_df.loc[billcharges_vendedoras_df["formatted_date"] == seletor_dia]
    groupby_quote_dia = billcharges_vendedoras_df_dia.groupby(['quote_id','customer_id']).agg({'amount': 'sum', 'avista': 'sum'}).reset_index()
    
    with resumo_1:
      
      st.dataframe(groupby_quote_dia,hide_index=True,use_container_width=True,column_config=column_config)
    
    with resumo_2:
      total_sales_dia = groupby_quote_dia["amount"].sum()
      total_avista_dia = groupby_quote_dia["avista"].sum()
      total_vendas_dia = groupby_quote_dia["quote_id"].count()

      st.metric(label="Quantidade de vendas", value=total_vendas_dia)
      st.metric(label="Vendas Total (R$)", value=f"R$ {total_sales_dia:,.2f}")
      st.metric(label="Vendas à vista (R$)", value=f"R$ {total_avista_dia:,.2f}")
      


    error_page = False

if error_page:
  st.title("Página não encontrada")
