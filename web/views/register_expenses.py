from web.api_client import HomeSplitApi
import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
import time


def register_expense():
    load_dotenv()

    types_category = pd.DataFrame({'Categorias de despesa': [
        'Mercado', 'Internet', 'Aluguel', 'Pets', 'Energia', 'Água', 'Manutenção']})

    BASE_URL = os.getenv('BASE_URL')

    api_client = HomeSplitApi(BASE_URL)

    st.title('Cadastro de Despesas')

    with st.form("form_despesa", clear_on_submit=True):
        st.subheader("Nova Despesa")
        token = st.session_state["access_token"]
        expense_value = st.number_input('Valor da despesa')
        category = st.selectbox('Selecione a categoria da despesa',
                                types_category['Categorias de despesa'])
        descrption = st.text_area('Descrição da despesa')
        if st.form_submit_button("Cadastrar Despesa"):
            with st.spinner('Cadastrando despesa'):
                response = api_client.register_expense(token,
                                                       expense_value, descrption, category)

            if response.status_code == 201:
                st.success("Despesa enviada e campos limpos!")

            elif response.status_code != 201:
                erro = response.json().get("message")
                st.error(f"🚫 {erro}")
