from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np
import joblib


from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# constants
#TEXT_COLUMNS = ["title","artist_name","release","artist_terms","similar_artists","location"]
TEXT_COLUMNS = ["title","artist_terms"]
NUMERIC_COLUMNS = ["duration","tempo","loudness","key","mode","time_signature"]

SAVE_DIR  = "_Recommendation_System_\\models"


def build_features(df: pd.DataFrame): # Forces pandas dataframe as input
    """Function for building features from the original dataset"""
    
    # Numeric columns
    df_num = df[NUMERIC_COLUMNS].fillna(0)

    scaler = StandardScaler()
    X_num = scaler.fit_transform(df_num)
    
    # Vectorize the text columns
    vectorizer = TfidfVectorizer(max_features=20000)

    data = df[TEXT_COLUMNS].fillna("").agg(" ".join, axis=1)
    vector = vectorizer.fit_transform(data)

    svd = TruncatedSVD(n_components=512, random_state=42)
    X_text = svd.fit_transform(vector)

    X_final = np.hstack([X_num, X_text])


    joblib.dump(X_final, f"{SAVE_DIR}/X_final.jb")
    joblib.dump(df, f"{SAVE_DIR}/df.jb")
    joblib.dump(vectorizer, f"{SAVE_DIR}/vectorizer.jb")
    joblib.dump(svd, f"{SAVE_DIR}/svd.jb")
    joblib.dump(scaler, f"{SAVE_DIR}/scaler.jb")
    return X_final, df


def cluster_data(final_scaled, df, n_clusters=20):
    """Function for clustering the songs using KMeans"""
    kmeans = KMeans(
        n_clusters=n_clusters,
        init="k-means++",
        n_init=20,
        max_iter=300,
        random_state=42
    )
    labels = kmeans.fit_predict(final_scaled)

    df['cluster'] = labels

    # Save the data
    np.savez_compressed(f"{SAVE_DIR}/clusters.npz", df['cluster'].values)
    joblib.dump(kmeans, f"{SAVE_DIR}/kmeans.jb")
    joblib.dump(df, f"{SAVE_DIR}/df.jb")
    df.to_csv(f"{SAVE_DIR}/df.csv")


if __name__ == "__main__":
    df = pd.read_csv("output.csv")

    scaled, df = build_features(df)
    cluster_data(scaled, df)