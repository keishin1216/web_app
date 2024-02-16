import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Book2.csvからDTW距離のデータを読み込む
dtw_data = pd.read_csv('../eda改/dtw.csv')

# クラスタリングのためのKMeansモデルを作成
kmeans = KMeans(n_clusters=2, random_state=42)

# モデルにデータを適合
kmeans.fit(dtw_data[['dtw(正規化)']])

# クラスタリングの結果を取得
labels = kmeans.labels_

# 各データにクラスタ情報を追加
dtw_data['Cluster'] = labels

# クラスタリングの結果を表示
print("クラスタリング結果:")
print(dtw_data)

# クラスタごとにデータ数を表示
print("\n各クラスタのデータ数:")
print(dtw_data['Cluster'].value_counts())


# クラスタごとに色を指定
colors = ['red', 'blue']

# データをプロット
plt.scatter(dtw_data['username'], dtw_data['dtw(正規化)'], c=dtw_data['Cluster'].map({0: colors[0], 1: colors[1]}))
plt.xlabel('Name')
plt.ylabel('dtw(正規化)')
plt.title('Clustering Result')

# x軸のラベルを回転して読みやすくする
plt.xticks(rotation=45, ha='right')

# 各データポイントに対してテキストを追加
for i, txt in enumerate(dtw_data['dtw(正規化)']):
    plt.text(i, dtw_data['dtw(正規化)'][i], f"{txt:.2f}", ha='left', va='bottom')

plt.show()

