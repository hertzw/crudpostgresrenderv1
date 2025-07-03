import psycopg2
import streamlit as st

class repositorio():
    mydb = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        dbname=st.secrets["postgres"]["database"],
        port=st.secrets["postgres"]["port"]
    )
    cursor = mydb.cursor()


