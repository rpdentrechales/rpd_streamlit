import streamlit as st

# --- PAGE SETUP ---
visualizar_page = st.Page(
    "views/visualisar.py",
    title="Visualizar Vendas",
    icon=":material/point_of_sale:",
    default=True,
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Pages": [visualizar_page]
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")


# --- RUN NAVIGATION ---
pg.run()
