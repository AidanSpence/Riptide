from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("1015_output.csv")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["title"])

df = df.drop(["title","artist_name","release","artist_terms","similar_artists","location"], axis=1)
title_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
final_df = pd.concat([df, title_df], axis=1)

kmeans = KMeans(
    n_clusters=10,
    random_state=42
)

clusters = kmeans.fit_predict(final_df)

centroids = kmeans.cluster_centers_


pca = PCA()
reduced_features = pca.fit_transform(final_df)
reduced_centroids = pca.transform(kmeans.cluster_centers_)

plt.figure(figsize=(10, 7))
plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=clusters, cmap='tab10', s=30, alpha=0.6)
plt.scatter(reduced_centroids[:, 0], reduced_centroids[:, 1], marker='X', s=200, c='red', label='Centroids')

plt.title("K-Means: Song Clusters (PCA Reduced)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
plt.show()