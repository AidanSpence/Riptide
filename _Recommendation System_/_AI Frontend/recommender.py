from sklearn.metrics.pairwise import cosine_similarity
import torch

# if song_name not in df['track_name'].values:
#     return "Song not found"

model = torch.load("_Recommendation System/models/model.mo")


similarity_matrix = cosine_similarity(embeddings)
