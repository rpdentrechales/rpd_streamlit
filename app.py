import streamlit as st

# --- PAGE SETUP ---
visualizar_page = st.Page(
    "views/visualisar.py",
    title="Visualizar Vendas",
    icon=":material/point_of_sale:"
)
configurar_page = st.Page(
    "views/configurar_vendedoras.py",
    title="Configurar Vendedoras",
    icon=":material/manufacturing:",
    default=True
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Área de Vendedora": [visualizar_page],
        "Testes": [configurar_page]
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")


# --- RUN NAVIGATION ---
pg.run()
