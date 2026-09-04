import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Carregar os dados sintéticos
df = pd.read_csv('historico_bueiros_sp.csv')

# 2. Separar as variáveis de entrada (X) e o alvo (y)
X = df[['obstrucao_sensor_percentual', 'previsao_chuva_24h_mm', 'historico_alagamento_regiao']]
y = df['risco_enchente_alvo']

# 3. Dividir os dados: 80% para treino, 20% para teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Treinar o modelo Random Forest
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)

# 5. Avaliar a Acurácia
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do Modelo: {accuracy * 100:.2f}%")

# 6. Salvar o modelo treinado para o Dashboard
joblib.dump(rf_model, 'modelo_bueiros.pkl')