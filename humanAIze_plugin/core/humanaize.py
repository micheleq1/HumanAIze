import os

import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Calcola il percorso assoluto di dataset.csv
base_dir = os.path.dirname(__file__)  # Directory in cui si trova humanaize.py
dataset_path = os.path.join(base_dir, "../data/dataset.csv")

# Carica il dataset
df = pd.read_csv(dataset_path)


# Carica il dataset
#df = pd.read_csv('../data/dataset.csv')

# Riempi i NaN con mediana (per le colonne numeriche) o moda (per le colonne categoriche)


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
def visualizza_confronto_log(y_pred_original, y_test_original, targets, num_samples=5):
    """
    Stampa il confronto tra predizioni e valori reali tramite log.message.

    Parameters
    ----------
    y_pred_original : ndarray
        Valori predetti (denormalizzati).
    y_test_original : ndarray
        Valori reali (denormalizzati).
    targets : list
        Lista dei nomi dei target.
    num_samples : int
        Numero di campioni da includere nel log.
    """
    print("\nConfronto tra predizioni e valori reali per alcuni campioni:")
    for i in range(num_samples):  # Mostra i primi 'num_samples' campioni
        print(f"\nTest Sample {i + 1}:")
        for j, target in enumerate(targets):
            print(
                f"  {target}: Predizione = {y_pred_original[i, j]:.4f}, Reale = {y_test_original[i, j]:.4f}"
            )



