import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from src.week1.jaimil_db_utilities import fetchall
from src.week3.jaimil_features import FEATURES, TARGET, NUMERIC, CATEGORICAL

def load(table):
    rows = fetchall(f"SELECT {','.join(FEATURES+[TARGET])} FROM {table};")
    return pd.DataFrame(rows)

def run():
    df = load("training_data")
    X = df[FEATURES]
    y = (df[TARGET] == ">50K").astype(int)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pre = ColumnTransformer([
        ("num", "passthrough", NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    model = Pipeline([
        ("pre", pre),
        ("clf", RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)),
    ])
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    print("RF holdout accuracy:", accuracy_score(yte, pred))

if __name__ == "__main__":
    run()