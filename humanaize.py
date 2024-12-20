import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Carica il dataset
df = pd.read_csv('dataset.csv')

# Definire i target numerici
targets = [
    "gender", "age", "muscle", "weight", "height", "proportions",
    "african", "asian", "caucasian", "breast_size", "breast_firmness",
    "vertical_position", "horizontal_distance", "pointiness", "breast_volume",
    "nipple_size", "nipple_point", "face_age", "face_head_fat", "face_angle",
    "face_oval", "face_round", "face_rectangular", "face_square", "face_triangular",
    "face_invertedtriangular", "face_diamond", "torso_scale_depht",
    "torso_scale_horizontally", "torso_scale_vertically", "torso_move_horizontally",
    "torso_move_depht", "torso_scale_cone_shape", "torso_dorsi_muscle",
    "torso_pectoral_muscle", "fingers_distance", "fingers_diameter",
    "fingers_lenght", "scale_hand", "hand_position", "neck_circum", "neck_height"
]

# Preprocessing del testo (descrizione) usando TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)  # Imposta il numero massimo di features da estrarre
X_text = vectorizer.fit_transform(df["descrizione"])

# Preprocessing dei target (normalizzazione)
scaler = StandardScaler()
y = scaler.fit_transform(df[targets])

# Divisione in train/test
X_train, X_test, y_train, y_test = train_test_split(X_text, y, test_size=0.1, random_state=23)

# Modello di Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=23)
model.fit(X_train, y_train)

# Previsione sui dati di test
y_pred = model.predict(X_test)

# Invertire la normalizzazione per ottenere i valori originali
y_pred_original = scaler.inverse_transform(y_pred)

# Calcolo dell'errore (MSE) sui target numerici
mse = mean_squared_error(y_test, y_pred_original)
print(f"Errore quadratico medio: {mse}")

# Visualizzare le previsioni
for i, num_pred in enumerate(y_pred_original):
    print(f"Test Sample {i + 1}:")
    print(f"  Predizione: {num_pred}")
    print(f"  Valore reale: {scaler.inverse_transform([y_test[i]])[0]}")
