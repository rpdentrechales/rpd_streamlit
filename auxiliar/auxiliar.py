from pymongo import MongoClient, UpdateOne
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def get_dataframe_from_mongodb(collection_name, database_name, query={}):

    client = MongoClient(f"mongodb+srv://rpdprocorpo:iyiawsSCfCsuAzOb@cluster0.lu6ce.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client[database_name]
    collection = db[collection_name]

    data = list(collection.find(query))

    if data:
        dataframe = pd.DataFrame(data)
        if '_id' in dataframe.columns:
            dataframe = dataframe.drop(columns=['_id'])
    else:
        dataframe = pd.DataFrame()

    return dataframe

def plot_sales_count(df):
    df['date'] = pd.to_datetime(df['date'])
    df['formatted_date'] = df['date'].dt.strftime('%d/%m/%Y')

    daily_metrics = df.groupby('formatted_date').agg(
        sales_count=('quote_id', 'nunique')
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily_metrics['formatted_date'],
        y=daily_metrics['sales_count'],
        name='Quantidade de Vendas',
        marker_color='blue'
    ))
    fig.update_layout(
        title="Quantidade de vendas por dia",
        xaxis_title="Dia",
        yaxis_title="Quantidade de vendas",
        xaxis=dict(tickangle=-45)
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_total_sales(df):

    df['date'] = pd.to_datetime(df['date'])
    df['formatted_date'] = df['date'].dt.strftime('%d/%m/%Y')

    daily_metrics = df.groupby('formatted_date').agg(
        total_sales=('amount', 'sum'),
        total_sales_avista=('avista', 'sum')
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily_metrics['formatted_date'],
        y=daily_metrics['total_sales'],
        name='Total de Vendas (R$)',
        marker_color='green'
    ))
    fig.add_trace(go.Bar(
        x=daily_metrics['formatted_date'],
        y=daily_metrics['total_sales_avista'],
        name='Total Vendas Avista (R$)',
        marker_color='orange'
    ))
    fig.update_layout(
        title="Valor vendido por dia (total e à vista)",
        xaxis_title="Dia",
        yaxis_title="Total de vendas (R$)",
        xaxis=dict(tickangle=-45),
        barmode='group' 
    )

    st.plotly_chart(fig, use_container_width=True)
