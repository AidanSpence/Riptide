import torch
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from _Recommendation_System_.Backend.model import TripletNet

class SongRecommender:
    def __init__(self, input_dim, device="cpu"):
        self.device = device

        self.model = TripletNet(input_dim).to(device)
        self.model.load_state_dict(torch.load("_Recommendation_System_/models/model.pt", map_location=device))
        self.model.eval()

        self.embeddings = np.load("_Recommendation_System_/models/embeddings.npy")
        self.df = joblib.load("_Recommendation_System_/models/df.joblib")

    def recommend(self, query_vector, k=10):
        with torch.no_grad():
            q = torch.tensor(query_vector, dtype=torch.float32).unsqueeze(0)
            query_emb = self.model(q.to(self.device)).cpu().numpy()

        # similarity ranking
        scores = cosine_similarity(query_emb, self.embeddings)[0]
        top_k = np.argsort(scores)[::-1][:k]

        return self.df.iloc[top_k]