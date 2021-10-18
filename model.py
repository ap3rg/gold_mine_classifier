# general imports
import os
import pickle
import pandas as pd

## imports for classification
from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import train_test_split

# local imports
import config as conf
import constants as const 

# Load mine spectral data
df_spectral_raw = pd.read_csv(conf.spectral)
df_spectral_raw = df_spectral_raw[const.classification_bands].copy()
df_spectral = pd.DataFrame(columns=const.classification_bands)

for col in df_spectral_raw.columns:
    raw_data = df_spectral_raw[col].item()[1:-1]
    raw_data = raw_data.strip().split(",")
    data = [d.strip() for d in raw_data]
    df_spectral[col] = pd.Series(data)

df_spectral["class"] = 1

# Load control spectral data
df_control_raw = pd.read_csv(conf.control)
df_control_raw = df_control_raw[const.classification_bands].copy()
df_control = pd.DataFrame(columns=const.classification_bands)

for col in df_control_raw.columns:
    raw_data = df_control_raw[col].item()[1:-1]
    raw_data = raw_data.strip().split(",")
    data = [d.strip() for d in raw_data]
    df_control[col] = pd.Series(data)

df_control["class"] = 0

df_dataset = pd.concat([df_spectral, df_control])

print("Dropping NaN")
print(df_dataset.isna().sum())
df_dataset.dropna(inplace=True)

X = df_dataset[const.classification_bands].values.reshape(-1, len(const.classification_bands))
y = df_dataset["class"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

print(f'Training model with {X_train.shape[0]} samples and {len(const.classification_bands)} features.')

model = svm.SVC(gamma='scale')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\tAccuracy:", metrics.accuracy_score(y_test, y_pred))
print("\tPrecision:", metrics.precision_score(y_test, y_pred))
print("\tRecall:", metrics.recall_score(y_test, y_pred))

# save model

with open(os.path.join(conf.model_path, "model.pkl"), 'wb') as f:
    pickle.dump(model, f)