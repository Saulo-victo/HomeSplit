# Home Split

#### Desenvolvimento de uma API rest para controle de despesas caseiras com autenticação de uusário (JWT), lançamento de despesas, dashboard interativo para análise de despesas mensais conjuntas, tratamento de erros, persistência em banco de dados relacional. Front-End mínimo utilizando streamlit. 

## 🚀Funcionalidades Principais

- Autenticação de usuários (JWT)
- Cadastro de despesas
- Dahsboardo com acesso as transaçõe do mês ou outro de referência
- Persistência com banco relacional

## 💡Futuras funcionalidades
- Isolamento de residência por grupo de usuários
- Edição de despesas;
- Cadastro de categorias de despesas

## 🛠️ Tecnologias

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Streamlit

## 📁Arquitetura de projeto

``` src/ 
├── api/ # Camada de entrada (rotas HTTP)
├── application/ # Casos de uso
├── domain/ # Regras de negócio
└── infrastructure/ # Banco, segurança, etc.
```

## ⚙️Como rodar
1. Crie um clone do repositório
<pre> git clone https://github.com/Saulo-victo/HomeSplit.git </pre>

2. Crie um ambiente virtual para execução
<pre> python3 -m venv nome_do_ambiente_virtual </pre>

3. Ative o ambiente virtual
<pre> windows: ./nome_do_ambiente_virtual/Scripts/activate </pre>
<pre> linux: source ./nome_do_ambiente_virtual/bin/activate </pre>

4. Instale os requirements.txt
<pre> pip install -r requirements.txt </pre>

5. Configure as variáveis de ambiente presentes no diretório, substituindo a string SQL_ALCHEMY_DATABASE_URL por um banco de dados postgres criado
<pre>"postgresql+psycopg2://(user):(passowrd)@localhost:5432/(BdName)</pre>
Atenção: Basta conectar com um banco existente, o SqlAlchemy cuidará da criação das tabelas

6. Rode o arquivo start.py
<pre>python3 -m start</pre>

## 🎥Demonstração

- Tela de autenticação do usuário:
  
![gif01](https://github.com/user-attachments/assets/9c4809a8-937c-4de0-8bc9-d4216a45466e)

- Tela de cadastro de despesa
  
![gif02](https://github.com/user-attachments/assets/60600c69-fc98-47c2-891e-f0eacb6af422)

- Exclusão de despesa e filtro por mês
  
![gif03](https://github.com/user-attachments/assets/92fa196f-a004-4046-95c2-603312c4db81)

- API Documentada via swegger com os endpoints
  
![gif04](https://github.com/user-attachments/assets/b161aa04-b726-4f14-8842-5cc6d94363ed)




“Melhoria contínua é melhor do que perfeição adiada.” — Mark Twain
#### Desenvolvido por Saulo Victo Soares.

























