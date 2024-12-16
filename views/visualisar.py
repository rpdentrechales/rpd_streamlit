import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from auxiliar.auxiliar import *
import plotly.express as px

st.set_page_config(page_title="Pró-Corpo - Visualizar Vendas", page_icon="💎",layout="wide")

st.title("Visualizar Vendas")
