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
    def __init__(self, input_dim, device="cpu"):
        self.device = device

        self.model = TripletNet(input_dim).to(device)
        self.model.load_state_dict(torch.load(MODELS_PATH / "model.pt", map_location=device, weights_only=True))
        self.model.eval()
        npz_file = np.load(MODELS_PATH / "embeddings.npz")
        self.embeddings = npz_file['embeddings']
        self.df = joblib.load(MODELS_PATH / "df.jb")

    def recommend(self, query_vector, k=10, temperature=0.1):
        with torch.no_grad():
            print("in recommend")
            q = torch.tensor(query_vector, dtype=torch.float32).unsqueeze(0)

            noise = torch.randn_like(q) * temperature
            q_noisy = q + noise

            q_sliced = q_noisy[:,:518]
            query_emb = self.model(q_sliced.to(self.device)).cpu().numpy()

        # similarity ranking
        N = 100
        scores = cosine_similarity(query_emb, self.embeddings)[0]
        top_n = np.argsort(scores)[::-1][:N]

        top_scores = scores[top_n]
        probs = top_scores / top_scores.sum()

        chosen = np.random.choice(top_n, size=k, replace=False, p=probs)

        subset = self.df.iloc[chosen].reset_index(drop=True)

        output = pd.DataFrame({
            'Title': subset['title'],
            'Artist': subset['artist_name']
        })

        return output.to_html(
            classes='recommendation-table',
            index=False
        )