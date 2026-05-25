from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import joblib

# constants
TEXT_COLUMNS = ["title","artist_name","release","artist_terms","similar_artists","location"]
SAVE_DIR  = "_Recommendation_System_\models"

# variables
vectorizer = TfidfVectorizer()

# datasets

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
df_scaled = scaler.fit_transform(final_df)

print("scaled")

# Cluster the songs using KMeans
kmeans = KMeans(
    n_clusters=20,
    random_state=42
)

print("kmeans")

embeddings = model(torch.tensor(final_df_scaled, dtype=torch.float32)).detach().cpu().numpy()
kmeans.fit(embeddings)
df['cluster'] = kmeans.labels_

print("fit")

# Save the data
np.savez_compressed(f"{save_dir}/clusters.npz", df['cluster'].values)
joblib.dump(kmeans, f"{save_dir}/kmeans.jb")
joblib.dump(df_scaled, f"{save_dir}/scaler.jb")


if __name__ == "__main__":
    df = pd.read_csv("output.csv")