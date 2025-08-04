import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="Score de Crédito QuantumFinance", layout="wide")

st.title("Sistema de Score de Crédito")
st.markdown("Insira os dados do cliente para obter uma estimativa do score de crédito.")

with st.form(key='credit_form'):
    st.subheader("Dados do Cliente")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Idade", min_value=18, max_value=100, value=30)
        occupation = st.selectbox("Ocupação", ["Software Engineer", "Teacher", "Doctor", "Scientist", "Lawyer", "Accountant", "Developer", "Manager", "Entrepreneur", "Media Manager", "Musician", "Mechanic", "Journalist", "Architect", "Writer", "Credit Analyst", "Financial Analyst"])
        annual_income = st.number_input("Renda Anual ($)", min_value=10000, value=75000)
        monthly_inhand_salary = st.number_input("Salário Mensal Líquido ($)", min_value=500, value=5000)
        num_bank_accounts = st.number_input("Nº de Contas Bancárias", min_value=0, max_value=20, value=2)
        num_credit_card = st.number_input("Nº de Cartões de Crédito", min_value=0, max_value=20, value=3)
        interest_rate = st.number_input("Taxa de Juros (%)", min_value=1, max_value=35, value=15)
        num_of_loan = st.number_input("Nº de Empréstimos", min_value=0, max_value=10, value=2)
        delay_from_due_date = st.number_input("Atraso de Pagamento (dias)", min_value=0, max_value=100, value=20)
        num_of_delayed_payment = st.number_input("Nº de Pagamentos Atrasados", min_value=0, max_value=50, value=10)
    
    with col2:
        num_credit_inquiries = st.number_input("Consultas de Crédito (últimos 6 meses)", min_value=0, max_value=20, value=5)
        credit_mix = st.selectbox("Mix de Crédito", ["Good", "Standard", "Bad"])
        outstanding_debt = st.number_input("Dívida Pendente ($)", min_value=0, value=5000)
        credit_utilization_ratio = st.number_input("Taxa de Utilização de Crédito (%)", min_value=0.0, max_value=100.0, value=30.0)
        credit_history_age = st.selectbox("Idade do Histórico de Crédito", ["2 Years", "5 Years", "10 Years"])
        payment_of_min_amount = st.selectbox("Pagamento Mínimo", ["Yes", "No"])
        total_emi_per_month = st.number_input("EMI Total por Mês ($)", min_value=0, value=500)
        amount_invested_monthly = st.number_input("Valor Investido Mensal ($)", min_value=0, value=200)
        payment_behaviour = st.selectbox("Comportamento de Pagamento", ["High Spend", "Low Spend", "Average Spend", "Good Spend", "Not Specified"])
        monthly_balance = st.number_input("Balanço Mensal ($)", min_value=0, value=1000)
    
    submitted = st.form_submit_button("Prever Score")

if submitted:
    url = "http://localhost:8000/predict_score"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "Age": age, "Occupation": occupation, "Annual_Income": annual_income, "Monthly_Inhand_Salary": monthly_inhand_salary,
        "Num_Bank_Accounts": num_bank_accounts, "Num_Credit_Card": num_credit_card, "Interest_Rate": interest_rate,
        "Num_of_Loan": num_of_loan, "Delay_from_due_date": delay_from_due_date, "Num_of_Delayed_Payment": num_of_delayed_payment,
        "Num_Credit_Inquiries": num_credit_inquiries, "Credit_Mix": credit_mix, "Outstanding_Debt": outstanding_debt,
        "Credit_Utilization_Ratio": credit_utilization_ratio, "Credit_History_Age": credit_history_age,
        "Payment_of_Min_Amount": payment_of_min_amount, "Total_EMI_per_month": total_emi_per_month,
        "Amount_invested_monthly": amount_invested_monthly, "Payment_Behaviour": payment_behaviour,
        "Monthly_Balance": monthly_balance
    }

    st.subheader("Resultado da Previsão")
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            score = result.get("credit_score")
            st.success(f"O score de crédito previsto é: **{score}**")
        elif response.status_code == 401:
            st.error("Erro de Autenticação: Chave de API inválida. Verifique o seu `.env`.")
        else:
            st.error(f"Erro na API: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão: A API não está em execução ou o endereço está incorreto.")