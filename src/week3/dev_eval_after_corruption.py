import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.week1.jaimil_db_utilities import fetchall
from src.week3.jaimil_features import FEATURES, TARGET, NUMERIC, CATEGORICAL


def load(table):
    rows = fetchall(f"SELECT {','.join(FEATURES+[TARGET])} FROM {table};")
    return pd.DataFrame(rows)


def build_model(train_df):
    X = train_df[FEATURES]
    y = (train_df[TARGET] == ">50K").astype(int)

    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    pre = ColumnTransformer([
        ("num", num_pipe, NUMERIC),
        ("cat", cat_pipe, CATEGORICAL),
    ])

    model = Pipeline([
        ("pre", pre),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    return model.fit(X, y)


def run(seed=42):
    rng = np.random.default_rng(seed)

    train_df = load("training_data")
    prod_df = load("production_data")

    model = build_model(train_df)

    X = prod_df[FEATURES].copy()
    y = (prod_df[TARGET] == ">50K").astype(int)

    base = accuracy_score(y, model.predict(X))
    print("Base prod accuracy:", base)

    impacts = []
    for col in FEATURES:
        Xp = X.copy()
        Xp[col] = rng.permutation(Xp[col].values)
        acc = accuracy_score(y, model.predict(Xp))
        impacts.append((col, base - acc))

    impacts.sort(key=lambda x: x[1], reverse=True)

    print("\nFeature impact (accuracy drop when permuted):")
    for col, drop in impacts:
        print(f"{col:<16} {drop:.6f}")


if __name__ == "__main__":
    run()