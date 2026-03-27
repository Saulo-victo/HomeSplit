import streamlit as st
from web.views.login import login_page
from web.views.register_expenses import register_expense

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None


def main():
    st.set_page_config(
        page_title="HomeSplit",
        page_icon="🧮",
        layout='centered')

    if "pagina_atual" not in st.session_state:
        st.session_state.pagina_atual = "Resumo"

    if st.session_state.get("access_token") is None:
        login_page()

    else:
        with st.sidebar:
            st.title("Home Split")
            if st.button("Resumo"):
                st.session_state.pagina_atual = "Resumo"
                st.rerun()

            if st.button("Lançar Despesa"):
                st.session_state.pagina_atual = "Lançar Despesa"
                st.rerun()

            if st.button("Sair"):
                st.session_state["access_token"] = None
                st.rerun()

        if st.session_state.pagina_atual == "Resumo":
            pass

        elif st.session_state.pagina_atual == "Lançar Despesa":
            register_expense()


if __name__ == "__main__":
    main()
