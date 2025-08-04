# Projeto MLOps: Score de Crédito para a QuantumFinance

## 1. Descrição do Projeto
Este projeto implementa um modelo de Machine Learning para prever o score de crédito de clientes. A solução abrange todo o ciclo de vida do modelo, desde o treinamento e versionamento até a disponibilização em uma API segura e um front-end em Streamlit.

**Objetivos:**
- Treinar um modelo de classificação de score de crédito.
- Utilizar MLflow para rastrear e versionar experimentos.
- Criar uma API segura (FastAPI) para servir o modelo.
- Desenvolver um aplicativo Streamlit para interagir com a API.
- Documentar o processo e a API.

## 2. Tecnologias Utilizadas
- **Linguagem:** Python
- **MLOps:** MLflow (Rastreamento e Versionamento)
- **Modelagem:** Scikit-learn
- **API:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **Containerização:** Docker
- **Gerenciamento de Pacotes:** pip

---

## 3. Guia Passo a Passo de Execução

### Passo 1: Configuração do Ambiente
1.  **Clone** este repositório para sua máquina local.
2.  **Baixe o dataset** `Credit_Score_Classification_Dataset.csv` do [Kaggle](https://www.kaggle.com/datasets/parisrohan/credit-score-classification) e coloque-o na pasta `data/raw/`.
3.  **Crie um ambiente virtual** para o projeto e ative-o.
    -   `python -m venv venv`
    -   `source venv/bin/activate` (Linux/macOS) ou `venv\Scripts\activate` (Windows)
4.  **Instale as dependências** do Python:
    -   `pip install -r requirements.txt`
5.  **Crie o arquivo `.env`** na raiz do projeto e adicione sua chave de API para segurança:
    -   `API_KEY="sua_chave_secreta_aqui"`

### Passo 2: Treinamento do Modelo
1.  Certifique-se de que o ambiente virtual está ativado.
2.  Execute o script de treinamento a partir do diretório raiz. Este script irá pré-processar os dados, treinar o modelo, salvar o `model.pkl` na raiz do projeto e rastrear o experimento com o MLflow.
    -   `python src/models/train_model.py`
3.  Para visualizar a interface do **MLflow UI**, execute o seguinte comando:
    -   `mlflow ui`
    -   Abra seu navegador e acesse `http://127.0.0.1:5000` para ver os experimentos.

### Passo 3: Execução da API (com Docker)
1.  Certifique-se de que o **Docker** está em execução em sua máquina.
2.  Construa a imagem Docker que contém a API:
    -   `docker build -t credit-score-api .`
3.  Execute o container da API. A porta 8000 do seu host será mapeada para a porta 8000 do container. A flag `--env-file` garante que sua chave de API seja carregada de forma segura.
    -   `docker run -d --rm -p 8000:8000 --env-file .env credit-score-api`
4.  A API estará disponível em `http://127.0.0.1:8000`.

### Passo 4: Execução da Aplicação Streamlit
1.  Verifique se a API está em execução (o container Docker deve estar ativo).
2.  Rode a aplicação Streamlit a partir do terminal.
    -   `streamlit run src/app/streamlit_app.py`
3.  O aplicativo web será aberto em seu navegador, permitindo que você interaja com a API localmente.

---

## 4. Documentação da API

A API foi construída com FastAPI, que gera automaticamente uma documentação interativa baseada no padrão OpenAPI (Swagger UI). Você pode acessá-la em seu navegador para testar o endpoint e entender os parâmetros de entrada e saída.

**Como Acessar:**
-   Com a API rodando, abra `http://127.0.0.1:8000/docs` em seu navegador.

**O que você vai encontrar:**
-   **Endpoint:** A documentação irá listar o endpoint `/predict_score`.
-   **Estrutura de Requisição (Request Body):** Você verá o esquema de dados (`CreditData`) necessário para fazer a previsão, com todos os campos e seus tipos.
-   **Campos da API Key:** A documentação indicará que a requisição exige um cabeçalho HTTP `x-api-key`.
-   **Teste Interativo:** Você pode usar a interface para enviar uma requisição de teste e ver a resposta da API em tempo real.