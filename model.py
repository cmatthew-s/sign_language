
'''
Resources to read:
https://datascience.stackexchange.com/questions/55066/how-to-export-pca-to-use-in-another-program
https://datascience.stackexchange.com/questions/55066/how-to-export-pca-to-use-in-another-program
'''

import pandas as pd
import pickle
import nltk
import json

from joblib import dump
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from GestureDetector import GestureDetector

gestureDetector = GestureDetector()
data = pd.read_csv('./data/Data_AI.csv')
df = data.drop(['type', 'category'], axis=1)
df = df.to_numpy()

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df.T).T

total_cat = len(data['category'].unique())
kmeans = KMeans(n_clusters=total_cat+1)
# label = kmeans.fit_predict(df_scaled_reduced)
label = kmeans.fit_predict(df_scaled)
pickle.dump(kmeans, open('./model/kmeans.pkl', 'wb'))

data['prediction'] = label
data.to_excel('./data/prediction.xlsx', index=False)

result = gestureDetector.get_result(data)
accuracy = gestureDetector.get_accuracy(data, result)
print(result)
print(accuracy)

with open('./data/result.txt', 'w') as fp:
    fp.write(json.dumps(result))
    
for key1 in result.keys():
    for key2 in result.keys():
        if result[key1] == result[key2]:
            if key1 != key2:
                print('{} = {}'.format(key1, key2))

