from sklearn.cluster import KMeans
import pandas

df = pandas.read_csv("output.csv")

df = df.drop(["title","artist_name","release","location"], axis=1)


kmeans = KMeans(
    n_clusters=10,
    random_state=42
)

df['cluster'] = kmeans.fit_predict(df)

print(df.head())