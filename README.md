# Home Split

#### Desenvolvimento de uma API rest para controle de despesas caseiras com autenticação de uusário (JWT), lançamento de despesas, dashboard interativo para análise de despesas mensais conjuntas, tratamento de erros, persistência em banco de dados relacional. Front-End mínimo utilizando streamlit. 

## 🚀Funcionalidades Principais

- Autenticação de usuários (JWT)
- Cadastro de despesas
- Dahsboardo com acesso as transaçõe do mês ou outro de referência
- Persistência com banco relacional

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
