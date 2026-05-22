from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import joblib

# constants
TEXT_COLUMNS = ["title","artist_name","release","artist_terms","similar_artists","location"]

# variables
vectorizer = TfidfVectorizer()

# datasets
df = pd.read_csv("output.csv")
word_df = df.copy()
dfs = {}

# Vectorize the text columns
def to_vectorize(location):
    data = df[location].fillna("").astype(str)
    x = vectorizer.fit_transform(data)
    return x

# Convert the vectorized data to DataFrames
def vector_to_df(vector):
    return pd.DataFrame(vector.toarray(), columns=vectorizer.get_feature_names_out())

# Vectorize the text columns and convert them to DataFrames
for column in TEXT_COLUMNS:
    print(f"Vectorizing {column}")
    vectorized = to_vectorize(column)
    dfs[column] = vector_to_df(vectorized)

# Drop the original text columns from the DataFrame
df = df.drop(TEXT_COLUMNS, axis=1)

# Concatenate the original DataFrame with the vectorized DataFrames
final_df = pd.concat([df] + list(dfs.values()), axis=1)

# Scale the features
scaler = StandardScaler()
final_df_scaled = scaler.fit_transform(final_df)

print("scaled")

# Cluster the songs using KMeans
kmeans = KMeans(
    n_clusters=20,
    random_state=42
)

print("kmeans")

kmeans.fit(final_df_scaled)
df['cluster'] = kmeans.labels_

print("fit")

# Save the models and data
joblib.dump(scaler, "_Recommendation System_/models/scaler.jb")
joblib.dump(kmeans, "_Recommendation System_/models/kmeans.jb")
joblib.dump(final_df_scaled, "_Recommendation System_/models/final_df_scaled.jb")
joblib.dump(df, "_Recommendation System_/models/df.jb")