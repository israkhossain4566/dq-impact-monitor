import pandas as pd

cols = ["age","workclass","fnlwgt","education","education_num","marital_status","occupation","relationship","race","sex","capital_gain","capital_loss",
"hours_per_week","native_country","income"]

#training data
train = pd.read_csv("data/raw/adult.data", header=None, names=cols, skipinitialspace=True)
train.to_csv("data/raw/adult_train.csv", index=False)

#testing data
test = pd.read_csv("data/raw/adult.test", header=None, names=cols, skiprows=1, skipinitialspace=True)
test.to_csv("data/raw/adult_prod.csv", index=False)

print("Train and Test datasets prepared successfully")
