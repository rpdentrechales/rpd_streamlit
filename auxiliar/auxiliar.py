from pymongo import MongoClient, UpdateOne
import pandas as pd
import streamlit as st
import plotly.express as px

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

def plot_daily_sales_metrics(df):
    """
    Plots a combined bar and line chart showing:
    - Daily sales count (unique quote_id),
    - Total sales (sum of amount),
    - Total avista sales (sum of avista).
    
    Args:
        df (pd.DataFrame): Input DataFrame with 'date', 'quote_id', 'amount', and 'avista' columns.
    """
    # Ensure 'date' is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Group data by 'date'
    daily_metrics = df.groupby('date').agg(
        sales_count=('quote_id', 'nunique'),
        total_sales=('amount', 'sum'),
        total_sales_avista=('avista', 'sum')
    ).reset_index()

    # Melt the DataFrame to long format for Plotly
    metrics_long = daily_metrics.melt(
        id_vars='date',
        value_vars=['sales_count', 'total_sales', 'total_sales_avista'],
        var_name='Metric',
        value_name='Value'
    )

    # Create the bar chart
    fig = px.bar(
        metrics_long,
        x='date',
        y='Value',
        color='Metric',
        title="Daily Sales Metrics",
        barmode='group'
    )

    # Add a line overlay for total sales
    fig.add_scatter(
        x=daily_metrics['date'], 
        y=daily_metrics['total_sales'], 
        mode='lines+markers', 
        name='Total Sales (Line)'
    )

    # Display the chart in Streamlit
    st.title("Sales Overview")
    st.plotly_chart(fig, use_container_width=True)
