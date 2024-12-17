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

def plot_daily_sales_metrics(df):
    # Ensure 'date' is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Group data by 'date'
    daily_metrics = df.groupby('date').agg(
        sales_count=('quote_id', 'nunique'),
        total_sales=('amount', 'sum'),
        total_sales_avista=('avista', 'sum')
    ).reset_index()

    # Create the figure
    fig = go.Figure()

    # Add sales_count as a bar chart
    fig.add_trace(go.Bar(
        x=daily_metrics['date'],
        y=daily_metrics['sales_count'],
        name='Sales Count',
        marker_color='blue'
    ))

    # Add total_sales as a line
    fig.add_trace(go.Scatter(
        x=daily_metrics['date'],
        y=daily_metrics['total_sales'],
        mode='lines+markers',
        name='Total Sales',
        line=dict(color='green')
    ))

    # Add total_sales_avista as a line
    fig.add_trace(go.Scatter(
        x=daily_metrics['date'],
        y=daily_metrics['total_sales_avista'],
        mode='lines+markers',
        name='Total Sales Avista',
        line=dict(color='orange')
    ))

    # Update layout for better visualization
    fig.update_layout(
        title="Daily Sales Metrics",
        xaxis_title="Date",
        yaxis_title="Values",
        barmode='group',
        legend=dict(x=0, y=1.0),
        xaxis=dict(type='category')
    )

    # Display the chart in Streamlit
    st.title("Sales Overview")
    st.plotly_chart(fig, use_container_width=True)
