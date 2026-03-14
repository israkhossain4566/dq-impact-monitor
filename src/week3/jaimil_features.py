FEATURES = [
    "age","workclass","fnlwgt","education","education_num","marital_status","occupation",
    "relationship","race","sex","capital_gain","capital_loss","hours_per_week","native_country"
]
TARGET = "income"

NUMERIC = ["age","fnlwgt","education_num","capital_gain","capital_loss","hours_per_week"]
CATEGORICAL = [c for c in FEATURES if c not in NUMERIC]
