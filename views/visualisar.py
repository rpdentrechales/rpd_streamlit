import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from auxiliar.auxiliar import *
import plotly.express as px

st.set_page_config(page_title="Pró-Corpo - Visualizar Vendas", page_icon="💎",layout="wide")

st.title("Visualizar Vendas")

vendedoras_df = get_dataframe_from_mongodb("vendedoras", "rpd_database")
billcharges_df = get_dataframe_from_mongodb("billcharges", "rpd_database")

st.dataframe(vendedoras_df)
st.dataframe(billcharges_df)
