import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder
import joblib
import mlflow
import mlflow.sklearn

def train_model():
    """
    Carrega os dados, pré-processa, treina um modelo de classificação,
    avalia e salva o modelo, registrando tudo com MLflow.
    """
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("Credit Score Classification")

    with mlflow.start_run():
        # 1. Carregar os dados
        try:
            df = pd.read_csv("data/raw/Credit_Score_Classification_Dataset.csv")
        except FileNotFoundError:
            print("Erro: Dataset não encontrado. Certifique-se de que o arquivo está em data/raw/.")
            return

        # 2. Pré-processamento
        df.fillna(df.mode().iloc[0], inplace=True)
        categorical_features = ['Occupation', 'Type_of_Loan', 'Credit_History_Age']
        for col in categorical_features:
            df[col] = LabelEncoder().fit_transform(df[col])

        # Separa features e target
        X = df.drop('Credit_Score', axis=1)
        y = df['Credit_Score']

        # Divisão em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 3. Treinamento do Modelo
        n_estimators = 100
        max_depth = 10
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)

        # 4. Avaliação
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        print(f"Acurácia: {accuracy:.2f}")
        print(f"F1-score: {f1:.2f}")

        # 5. Salvar e Registrar o Modelo
        model_path = "model.pkl"
        joblib.dump(model, model_path)
        mlflow.log_artifact(model_path)
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="CreditScoreModel"
        )
        print("Modelo treinado e registrado com sucesso no MLflow.")

if __name__ == "__main__":
    train_model()