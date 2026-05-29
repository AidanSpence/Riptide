import torch
import numpy as np
import joblib
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

        self.embeddings = np.load(MODELS_PATH / "embeddings.npz")
        self.df = joblib.load(MODELS_PATH / "df.jb")

    def recommend(self, query_vector, k=10):
        with torch.no_grad():
            q = torch.tensor(query_vector, dtype=torch.float32).unsqueeze(0)
            query_emb = self.model(q.to(self.device)).cpu().numpy()

        # similarity ranking
        scores = cosine_similarity(query_emb, self.embeddings)[0]
        top_k = np.argsort(scores)[::-1][:k]

        return self.df.iloc[top_k][["title", "artist_name"]]