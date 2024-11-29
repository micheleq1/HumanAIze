import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler,OneHotEncoder



df = pd.read_csv('dataset.csv')

# Preprocessing del testo
vectorizer = CountVectorizer()
X_text = vectorizer.fit_transform(df["descrizione"])
X_text_dense = X_text.toarray()
scaler = StandardScaler()
X_scaler=scaler.fit_transform(X_text_dense)
# Preprocessing dei target

y_numerical = scaler.fit_transform(df[["altezza", "peso"]])

# Encoding della variabile categoriale "capelli"
encoder = OneHotEncoder(sparse_output=False)
y_categorical = encoder.fit_transform(df[["capelli"]])

# Combiniamo i target numerici e categoriali
y_combined = np.hstack((y_numerical, y_categorical))

# Divisione in train/test
X_train, X_test, y_train, y_test = train_test_split(X_scaler, y_combined, test_size=0.1, random_state=23)

# Modello di regressione lineare
model = LinearRegression()
model.fit(X_train, y_train)

# Previsione sui dati di test
y_pred_scaled = model.predict(X_test)

# Separazione delle previsioni numeriche e categoriali
y_pred_numerical = scaler.inverse_transform(y_pred_scaled[:, :2])
y_pred_categorical = encoder.inverse_transform(y_pred_scaled[:, 2:])

# Ricomposizione dei risultati originali per il confronto
y_test_numerical = scaler.inverse_transform(y_test[:, :2])
y_test_categorical = encoder.inverse_transform(y_test[:, 2:])

# Calcolo dell'errore
mse = mean_squared_error(y_test_numerical, y_pred_numerical)
print(f"Errore quadratico medio: {mse}")

# Visualizzare le previsioni
for i, (num_pred, cat_pred) in enumerate(zip(y_pred_numerical, y_pred_categorical)):
    print(f"Test Sample {i + 1}:")
    print(f"  Predizione - Altezza: {num_pred[0]:.2f}, Peso: {num_pred[1]:.2f}, Capelli: {cat_pred}")
    print(f"  Valore reale - Altezza: {y_test_numerical[i][0]:.2f}, Peso: {y_test_numerical[i][1]:.2f}, Capelli: {y_test_categorical[i]}")

# Previsione per un nuovo input
input_text = ["genera una persona di altezza 1.84 di peso 93kg e capelli scuri"]
input_vectorizer = vectorizer.transform(input_text).toarray()
input_scaled = input_vectorizer

# Predizione
y_new_input_scaled = model.predict(input_scaled)

# Separazione della previsione numerica e categoriale
y_new_input_numerical = scaler.inverse_transform(y_new_input_scaled[:, :2])
y_new_input_categorical = encoder.inverse_transform(y_new_input_scaled[:, 2:])

# Risultato della previsione
print(f"Predizione per il nuovo input: Altezza - {y_new_input_numerical[0][0]:.2f}, Peso - {y_new_input_numerical[0][1]:.2f}, Capelli - {y_new_input_categorical[0]}")