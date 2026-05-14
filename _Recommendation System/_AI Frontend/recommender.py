from sklearn.metrics.pairwise import cosine_similarity

# if song_name not in df['track_name'].values:
#     return "Song not found"


similarity_matrix = cosine_similarity(embeddings)
