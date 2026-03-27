from web.api_client import HomeSplitApi
import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

meses = ["Janeiro", 'Fevereiro', 'Março', 'Abril', 'Maio',
         'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']


def dashboard_page():
    load_dotenv()

    BASE_URL = os.getenv('BASE_URL')

    api_client = HomeSplitApi(BASE_URL)

    column1row1, column2row1 = st.columns(2)

    with column1row1:
        st.title('🏠 Resumo geral')

    with column2row1:
        search_month = st.selectbox('Mês de referência', options=meses,
                                    index=(datetime.now().month-1))
        search_month_index = meses.index(search_month) + 1

    token = st.session_state["access_token"]
    response = api_client.get_data_sumary_month(token, search_month_index)

    if response:
        total_spend = response["total_spend"]
        top_category = response["top_category"]
        top_value_category = response["top_value_category"]
        total_by_category = response["total_by_category"]
        total_by_week = response["total_by_week"]
        list_expenses = response["list_expenses"]

    else:
        total_spend = 0
        top_category = '-'
        top_value_category = '-'
        total_by_category = '-'
        total_by_week = '-'
        list_expenses = '-'

    column1row2, column2row2, column3row2 = st.columns(3)

    with column1row2:
        with st.container(border=True):
            st.metric(label="Total Gasto (mês)", value=f'{total_spend} R$')

    with column2row2:
        with st.container(border=True):
            st.metric(label="Categoria mais gasta", value=top_category)

    with column3row2:
        with st.container(border=True):
            st.metric(label="Valor gasto com categoria mais cara",
                      value=top_value_category)

    column1row3, column2row3 = st.columns(2)

    with column2row3:
        data_week = [total_by_week['Semana 1'], total_by_week['Semana 2'],
                     total_by_week['Semana 3'], total_by_week['Semana 4']]

        chart_data = pd.DataFrame(
            data_week,
            index=['Semana 01', 'Semana 02', 'Semana 03', 'Semana 04']
        )
        with st.container(border=True):
            st.write('Evolução mensal dos gastos')
            st.line_chart(chart_data)

    with column1row3:
        with st.container(border=True):
            st.write('Gastos por categoria')
            chart_data_by_category = pd.DataFrame.from_dict(
                total_by_category, orient='index', columns=['Total'])
            st.bar_chart(chart_data_by_category)

    df = pd.DataFrame(list_expenses)

    if not df.empty:
        with st.container(border=True):
            mapping = {
                "date": "Data",
                "description": "Descrição",
                "expense_value": "Valor",
                "category": "Categoria",
                "name_user": "Quem Cadastrou"
            }

            df_transform = df[mapping.keys()].rename(columns=mapping)

            df_transform['Data'] = pd.to_datetime(
                df_transform['Data']).dt.strftime('%d/%m/%Y')

            st.subheader("Histórico Recente de Despesas")
            event = st.dataframe(
                df_transform,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                column_config={
                    "Valor": st.column_config.NumberColumn(
                        "Valor",
                        format="R$ %.2f",
                        help="Valor total da despesa"
                    )
                }
            )

            selected_rows = event.selection.rows

            if selected_rows:
                index = selected_rows[0]
                expense_id = df.loc[index]['id']
                expense_desc = df.loc[index]['description']

                print(expense_desc)
                print(expense_id)

                st.warning(f"Deseja excluir: **{expense_desc}**?")

                if st.button('Excluir', type='primary'):
                    response = api_client.delete_expense(token, expense_id)

                    if response.status_code == 200:
                        st.success("Excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error('Erro ao excluir')

    else:
        st.info('Nenhuma despesa encontrada para este mês 🍃')
