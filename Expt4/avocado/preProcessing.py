import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

dataset = pd.read_csv('avocado.csv')

dataset['Date'] = pd.to_datetime(dataset['Date']).astype(int)
dataset = dataset.drop(columns=['year'])
dataset = dataset[['Date'] + list(dataset.columns[3:]) + ['AveragePrice']]

X = dataset.iloc[:, :-1].values
Y = dataset.iloc[:, -1].values

labelencoder_X1 = LabelEncoder()
X[:, -1] = labelencoder_X1.fit_transform(X[:, -1])
labelencoder_X2 = LabelEncoder()
X[:, -2] = labelencoder_X2.fit_transform(X[:, -2])

imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(X[:, 1:-2])
X[:, 1:-2] = imputer.transform(X[:, 1:-2])

imputer1 = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
imputer1.fit(X[:, -2:-1])
X[:, -2:-1] = imputer1.transform(X[:, -2:-1])

pre_processed_dataset = pd.DataFrame(X, columns=dataset.columns[:-1])
pre_processed_dataset['AveragePrice'] = Y
pre_processed_dataset.to_csv('avocado_pre_processed.csv', index=False)
