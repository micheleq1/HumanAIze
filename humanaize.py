import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd
import numpy as np

# Carica il dataset
df = pd.read_csv('dataset.csv')

# Riempi i NaN con mediana (per le colonne numeriche) o moda (per le colonne categoriche)
for column in df.columns:
    if df[column].dtype in ['float64', 'int64']:  # Se la colonna è numerica
        df[column] = df[column].fillna(df[column].median())  # Usa mediana
    else:  # Se la colonna è categorica
        df[column] = df[column].fillna(df[column].mode()[0])  # Usa moda

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
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X_text = vectorizer.fit_transform(df["descrizione"])

# Preprocessing dei target (normalizzazione)
scaler = StandardScaler()
y = scaler.fit_transform(df[targets])

# Divisione in train/test
X_train, X_test, y_train, y_test = train_test_split(X_text, y, test_size=0.2, random_state=23)

# Convertire i dati in DMatrix per XGBoost
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Definire i parametri del modello XGBoost
params = {
    'objective': 'reg:squarederror',
    'eval_metric': 'mae',
    'max_depth': 6,
    'eta': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'seed': 23
}

# Addestrare il modello
num_rounds = 100
model = xgb.train(params, dtrain, num_rounds)

# Previsione sui dati di test
y_pred = model.predict(dtest)

# Invertire la normalizzazione per ottenere i valori originali
y_pred_original = scaler.inverse_transform(y_pred.reshape(-1, len(targets)))
y_test_original = scaler.inverse_transform(y_test)

# Calcolo della MAE per ogni target separatamente
print("MAE per ciascun target:")
mae_per_target = {}
for i, target in enumerate(targets):
    mae_target = mean_absolute_error(y_test_original[:, i], y_pred_original[:, i])
    mae_per_target[target] = mae_target
    print(f"  {target}: {mae_target:.4f}")

# Calcolo della MAE generale (aggregata su tutti i target)
mae_general = mean_absolute_error(y_test_original, y_pred_original)
print(f"\nMAE generale (aggregata): {mae_general:.4f}")


# Funzione per fare una previsione su un input personalizzato
def predizione_personalizzata(input_descrizione):
    # Preprocessing dell'input (descrizione) usando lo stesso TfidfVectorizer
    input_vec = vectorizer.transform([input_descrizione])

    # Convertire input_vec in DMatrix
    input_dmatrix = xgb.DMatrix(input_vec)

    # Previsione
    y_pred = model.predict(input_dmatrix)

    # Invertire la normalizzazione per ottenere i valori originali
    y_pred_original = scaler.inverse_transform(y_pred.reshape(1, -1))

    # Restituire la predizione
    return y_pred_original
# Funzione per visualizzare il confronto tra predizioni e valori reali
def visualizza_confronto(num_samples=5):
    print("\nConfronto tra predizioni e valori reali per alcuni campioni:")
    for i in range(num_samples):  # Mostra i primi 'num_samples' campioni
        print(f"\nTest Sample {i + 1}:")
        for j, target in enumerate(targets):
            print(f"  {target}: Predizione = {y_pred_original[i, j]:.4f}, Reale = {y_test_original[i, j]:.4f}")

# Visualizzare il confronto per i primi 5 campioni
visualizza_confronto(num_samples=20)

# Esempio di input personalizzato per fare una previsione
input_descrizione = input("\nInserisci una descrizione per la previsione: ")

# Fare la previsione sull'input
predizione = predizione_personalizzata(input_descrizione)

# Mostrare la predizione
print("\nPredizione per i target:")
for i, target in enumerate(targets):
    print(f"  {target}: {predizione[0, i]:.4f}")
# Funzione per aggiornare 'face_age' con i valori di 'age'
def aggiorna_face_age_con_age(df):
    df['face_age'] = df['age']  # Assegna i valori della colonna 'age' a 'face_age'
    return df

# Funzione per aggiornare 'face_age' con i valori di 'age' su tutto il dataset
def aggiorna_face_age_con_age(df):
    # Assicuriamoci che 'age' e 'face_age' siano presenti e che abbiano gli stessi valori
    if 'age' in df.columns and 'face_age' in df.columns:
        df['face_age'] = df['age']  # Assegna i valori della colonna 'age' a 'face_age'
    else:
        print("Le colonne 'age' e 'face_age' non sono presenti nel dataset.")
    return df

