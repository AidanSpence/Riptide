from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np
import joblib

# constants
TEXT_COLUMNS = ["title","artist_name","release","artist_terms","similar_artists","location"]
SAVE_DIR  = "_Recommendation_System_\\models"


def build_features(df: pd.DataFrame): # Forces pandas dataframe as input
    """Function for building features from the original dataset"""
    # Vectorize the text columns
    vectorizer = TfidfVectorizer(max_features=20000)
    
    dfs = {}

    for column in TEXT_COLUMNS:
        print(f"Vectorizing {column}")
        data = df[column].fillna("").astype(str)
        vector = vectorizer.fit_transform(data)

        dfs[column] = pd.DataFrame(vector.toarray(), columns=vectorizer.get_feature_names_out())

    # Drop the original text columns from the DataFrame and save to df_num
    df_num = df.drop(TEXT_COLUMNS, axis=1)
    # Concatenate the original DataFrame with the vectorized DataFrames
    final_df = pd.concat([df_num] + list(dfs.values()), axis=1)

    svd = TruncatedSVD(n_components=512)
    X_reduced = svd.fit_transform(final_df)

    # Scale the features
    scaler = StandardScaler()
    final_scaled = scaler.fit_transform(X_reduced)

    joblib.dump(final_scaled, f"{SAVE_DIR}/final_df_scaled.jb")

    return final_scaled, df


def cluster_data(final_scaled, df, n_clusters=20):
    """Function for clustering the songs using KMeans"""
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42
    )
    labels = kmeans.fit_predict(final_scaled)

    df['cluster'] = labels

    # Save the data
    np.savez_compressed(f"{SAVE_DIR}/clusters.npz", df['cluster'].values)
    joblib.dump(kmeans, f"{SAVE_DIR}/kmeans.jb")
    joblib.dump(df, f"{SAVE_DIR}/df.jb")


if __name__ == "__main__":
    df = pd.read_csv("output.csv")

    scaled, df = build_features(df)
    cluster_data(scaled, df)