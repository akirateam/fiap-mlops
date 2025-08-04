import os
import joblib
from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Inicializa o FastAPI
app = FastAPI(title="Credit Score API")

class CreditData(BaseModel):
    Age: int
    Occupation: str
    Annual_Income: int
    Monthly_Inhand_Salary: int
    Num_Bank_Accounts: int
    Num_Credit_Card: int
    Interest_Rate: int
    Num_of_Loan: int
    Delay_from_due_date: int
    Num_of_Delayed_Payment: int
    Num_Credit_Inquiries: int
    Credit_Mix: str
    Outstanding_Debt: int
    Credit_Utilization_Ratio: float
    Credit_History_Age: str
    Payment_of_Min_Amount: str
    Total_EMI_per_month: int
    Amount_invested_monthly: int
    Payment_Behaviour: str
    Monthly_Balance: int

try:
    model = joblib.load("model.pkl")
except FileNotFoundError:
    raise RuntimeError("Erro: 'model.pkl' não encontrado. Execute o script de treinamento primeiro.")

def preprocess_input(data: CreditData):
    df = pd.DataFrame([data.dict()])
    
    le = LabelEncoder()
    for col in ['Occupation', 'Type_of_Loan', 'Credit_History_Age']:
        df[col] = le.fit_transform(df[col])
        
    return df

@app.post("/predict_score", summary="Prever o Score de Crédito")
async def predict_credit_score(data: CreditData, x_api_key: str = Header(None)):
    """
    Endpoint para prever o score de crédito com base nos dados do cliente.
    Requer uma chave de API válida para autenticação.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de API inválida",
        )
    
    try:
        processed_data = preprocess_input(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro no pré-processamento: {e}"
        )

    prediction = model.predict(processed_data)
    score = int(prediction[0])

    return {"credit_score": score}

@app.get("/")
def read_root():
    return {"message": "API de Score de Crédito funcionando!"}