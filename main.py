import streamlit as st
from about_me import show_about_me
from recipe_app import run_recipe_app

st.set_page_config(page_title="Cook it Like There!", layout="wide")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["About Me", "Cook it Like There!"])

with tab1:
    show_about_me()

with tab2:
    run_recipe_app()
