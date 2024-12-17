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

    # Format date to show only dd/mm/yyyy
    df['formatted_date'] = df['date'].dt.strftime('%d/%m/%Y')

    # Group data by 'formatted_date'
    daily_metrics = df.groupby('formatted_date').agg(
        sales_count=('quote_id', 'nunique'),
        total_sales=('amount', 'sum'),
        total_sales_avista=('avista', 'sum')
    ).reset_index()

    # Create the figure
    fig = go.Figure()

    # Add total_sales as a bar
    fig.add_trace(go.Bar(
        x=daily_metrics['formatted_date'],
        y=daily_metrics['total_sales'],
        name='Total Sales',
        marker_color='green'
    ))

    # Add total_sales_avista as a bar
    fig.add_trace(go.Bar(
        x=daily_metrics['formatted_date'],
        y=daily_metrics['total_sales_avista'],
        name='Total Sales Avista',
        marker_color='orange'
    ))

    # Add sales_count as a bar, scaled for visibility
    fig.add_trace(go.Bar(
        x=daily_metrics['formatted_date'],
        y=daily_metrics['sales_count'],
        name='Sales Count',
        marker_color='blue'
    ))

    # Update layout: same axis, dual labels for clarity
    fig.update_layout(
        title="Daily Sales Metrics",
        xaxis_title="Date",
        yaxis=dict(
            title="Total Sales and Total Sales Avista",
        ),
        yaxis2=dict(
            title="Sales Count",
            overlaying="y",
            side="right",
            showgrid=False,
            range=[0, max(daily_metrics['sales_count'] * 1.1)]  # Scale for visibility
        ),
        barmode='group',  # Group bars side by side
        legend=dict(x=0, y=1.0)
    )

    # Display the chart in Streamlit
    st.title("Sales Overview")
    st.plotly_chart(fig, use_container_width=True)
