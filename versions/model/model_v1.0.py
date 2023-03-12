
'''
Resources to read:
https://datascience.stackexchange.com/questions/55066/how-to-export-pca-to-use-in-another-program
https://datascience.stackexchange.com/questions/55066/how-to-export-pca-to-use-in-another-program
'''

import pandas as pd
import pickle

from joblib import dump
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('./data/Data_AI.csv')
df = data.drop(['type', 'category'], axis=1)

# standardize values
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)
pickle.dump(scaler, open('./model/std_scaler.pkl', 'wb'))
# dump(scaler, './model/std_scaler.bin', compress=True)

# reduce dimensionality
pca = PCA(n_components=0.95, svd_solver='full')
df_scaled_reduced = pca.fit_transform(df_scaled)
print(df_scaled_reduced)
pickle.dump(pca, open('./model/pca.pkl', 'wb'))
# dump(pca, './model/pca.pkl', compress=True)

# applied clustering model
kmeans = KMeans(n_clusters=3)
label = kmeans.fit_predict(df_scaled_reduced)
pickle.dump(kmeans, open('./model/kmeans.pkl', 'wb'))
# dump(kmeans, './model/kmeans.pkl', compress=True)
data['prediction'] = label
data.to_excel('./data/prediction.xlsx', index=False)

