# Inicia o Backend em background
fastapi run src/api/main.py --port 8000 &

# Inicia o Frontend
streamlit run web/main_app.py --server.port 8080