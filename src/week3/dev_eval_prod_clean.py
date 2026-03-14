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
    rows = fetchall(f"SELECT {','.join(FEATURES + [TARGET])} FROM {table};")
    return pd.DataFrame(rows)


def train_model(train_df):
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


def run():
    train_df = load("training_data")
    prod_df = load("production_data")

    model = train_model(train_df)

    Xp = prod_df[FEATURES]
    yp = (prod_df[TARGET] == ">50K").astype(int)

    pred = model.predict(Xp)

    print("Prod accuracy (current state):", accuracy_score(yp, pred))


if __name__ == "__main__":
    run()