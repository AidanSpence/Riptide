import torch
import numpy as np
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from _Recommendation_System_.Backend.model import TripletNet
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_PATH = PROJECT_ROOT / "models"


class SongRecommender:
    """
    A class to generate song recommendations using a trained TripletNet neural network
    and cosine similarity on song embeddings.
    """
    def __init__(self, input_dim: int, device: str="cpu"):
        self.device = device

        # Initialize and load model
        self.model = TripletNet(input_dim).to(device)
        self.model.load_state_dict(torch.load(MODELS_PATH / "model.pt", map_location=device, weights_only=True))
        self.model.eval()

        # Load embeddings and song metadata
        npz_file = np.load(MODELS_PATH / "embeddings.npz")
        self.embeddings = npz_file['embeddings']
        self.df = joblib.load(MODELS_PATH / "df.jb")

    def recommend(
            self, 
            query_vector: np.array, 
            k: int = 10,
            temperature: int = 0.1,
            pool_size: int = 100,
            feature_dim: int = 518
            ):
        with torch.no_grad():
            q = torch.tensor(query_vector, dtype=torch.float32).unsqueeze(0)

            # Add random noise to improve variety
            noise = torch.randn_like(q) * temperature
            q_noisy = q + noise

            # Slice features and get model embedding
            q_sliced = q_noisy[:,:feature_dim]
            query_emb = self.model(q_sliced.to(self.device)).cpu().numpy()
        
        # Get top most similar songs
        similarity_scores = cosine_similarity(query_emb, self.embeddings)[0]
        top_indices = np.argsort(similarity_scores)[::-1][:pool_size]

        # Sample k songs using similarity scores as probabilities
        top_scores = similarity_scores[top_indices]
        probs = top_scores / top_scores.sum()
        chosen_indices = np.random.choice(top_indices, size=k, replace=False, p=probs)

        # Extract and format selected songs
        recommendations = self.df.iloc[chosen_indices][['title', 'artist_name']].rename(
            columns={'title': 'Title', 'artist_name': 'Artist'}
        )

        # Return the final results styled as an HTML table
        return recommendations.to_html(
            classes='recommendation-table',
            index=False
        )