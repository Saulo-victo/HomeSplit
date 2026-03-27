from web.api_client import HomeSplitApi
import streamlit as st
import os
from dotenv import load_dotenv


def login_page():
    load_dotenv()

    BASE_URL = os.getenv('BASE_URL')

    api_client = HomeSplitApi(BASE_URL)

    st.set_page_config(
        page_title="HomeSplit",
        page_icon="🧮",
        layout='wide'
    )

    st.title('HomeSplit - Gerenciador de Despesas Caseira')
    st.write("---")

    left_column, right_column = st.columns(2)

    with left_column:
        st.header('Login')
        user_email_login = st.text_input('Email', key='email_login')
        user_passowrd = st.text_input(
            'Senha', type='password', key='password_user')

        if st.button('Entrar'):
            with st.spinner('Entrando'):
                response = api_client.user_login(
                    user_email_login, user_passowrd)

            if response.status_code == 200:
                data = response.json()
                st.session_state["access_token"] = data["access_token"]
                st.session_state["user_email"] = user_email_login
                st.success("Login realizado com sucesso")
                st.rerun()

            elif response.status_code != 200:
                erro = response.json().get("message")
                st.error(f"🚫 {erro}")

    with right_column:
        st.header('Cadastro')
        user_name_register = st.text_input(
            'Nome de usuário', key='user_name_register')
        user_email_register = st.text_input('email', key='user_email_register')
        user_password_register = st.text_input(
            'Senha', type='password', key='user_password_register')
        if st.button('Cadastrar'):
            with st.spinner("Cadastrando"):
                response = api_client.user_register(
                    user_name_register, user_email_register, user_password_register)

            if response is None:
                st.error('Servidor fora do ar')

            elif response.status_code == 201:
                st.success('Usuário cadastrado')

            elif response.status_code != 201:
                erro = response.json().get("message")
                st.error(f"🚫 {erro}")
