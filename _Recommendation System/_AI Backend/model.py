import joblib
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from cluster import df

final_df_scaled = joblib.load("_Recommendation System/models/final_df_scaled.jb")

x_tensor = torch.tensor(final_df_scaled, dtype=torch.float32)

def create_triplets(X, labels):
    triplets = []

    label_to_indices = {}
    for i, label in enumerate(labels):
        label_to_indices.setdefault(label, []).append(i)

    indices = list(range(len(X)))

    for _ in range(len(x_tensor)):
        anchor = random.choice(indices)
        anchor_label = labels[anchor]

        positive = random.choice(label_to_indices[anchor_label])
        negative_index = random.choice([i for i in label_to_indices.keys() if i != anchor_label])
        negative = random.choice(label_to_indices[negative_index])

        triplets.append((anchor, positive, negative))

    return triplets

class TripletNet(nn.Module):
    def __init__(self, input_dim):
        super(TripletNet, self).__init__()
        self.stack = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 128))

    def forward(self, x):
        return self.stack(x)

model = TripletNet(final_df_scaled.shape[1])
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
criterion = nn.TripletMarginLoss(margin=1.0)

triplets = create_triplets(final_df_scaled, df['cluster'].values)

epochs = 10
for epoch in range(epochs):
    total_loss = 0
    for anchor, positive, negative in triplets:
        anchor_out = model(x_tensor[anchor])
        positive_out = model(x_tensor[positive])
        negative_out = model(x_tensor[negative])
    print("Done")