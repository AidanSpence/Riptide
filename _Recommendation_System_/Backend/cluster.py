import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD

# Constants
TEXT_COLUMNS = ["title","artist_name","artist_terms"]
NUMERIC_COLUMNS = ["duration","tempo","loudness","key","mode","time_signature"]

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent
SAVE_DIR = PROJECT_ROOT / "_Recommendation_System_" / "models"
SAVE_DIR.mkdir(parents=True, exist_ok=True)


def build_features(df: pd.DataFrame):
    """Extracts, scales, and vectorizes numeric and text features from the dataset"""
    
    # Process numeric features
    df_num = df[NUMERIC_COLUMNS].fillna(0)
    num_scaler = StandardScaler()
    X_num = num_scaler.fit_transform(df_num)
    
    # Process and vectorize text features
    vectorizer = TfidfVectorizer(max_features=20000)
    combined_text = df[TEXT_COLUMNS].fillna("").agg(" ".join, axis=1)
    text_vectors = vectorizer.fit_transform(combined_text)

    # Reduce text dimensionality using SVD
    svd = TruncatedSVD(n_components=512, random_state=42)
    X_text = svd.fit_transform(text_vectors)

    # Combine features
    X_final = np.hstack([X_num, X_text])

    # Save
    joblib.dump(df_num, SAVE_DIR / "df_num.jb")
    joblib.dump(vectorizer, SAVE_DIR / "vectorizer.jb")
    joblib.dump(svd, SAVE_DIR / "svd.jb")
    joblib.dump(num_scaler, SAVE_DIR / "num_scaler.jb")

    return X_final, df


def cluster_data(X_final: np.array, df: pd.DataFrame, n_clusters: int = 20):
    """Clusters the processed song features using KMeans and exports the final dataset"""

    kmeans = KMeans(
        n_clusters=n_clusters,
        init="k-means++",
        n_init=20,
        max_iter=300,
        random_state=42
    )
    labels = kmeans.fit_predict(X_final)
    df['cluster'] = labels

    # Save
    np.savez_compressed(SAVE_DIR / "clusters.npz", df['cluster'].values)
    joblib.dump(kmeans, SAVE_DIR / "kmeans.jb")
    joblib.dump(df, SAVE_DIR / "df.jb")
    joblib.dump(X_final, SAVE_DIR / "X_final.jb")
    df.to_csv(SAVE_DIR / "df.csv")


if __name__ == "__main__":
    # Load data
    raw_df = pd.read_csv("output.csv")

    # Run processing
    processed_features, processed_df = build_features(raw_df)
    cluster_data(processed_features, processed_df)

    print("Clustering complete and data saved.")