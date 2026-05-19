import joblib
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

# Load necessary variables
final_df_scaled = joblib.load("_Recommendation System/models/final_df_scaled.jb")
df = joblib.load("_Recommendation System/models/df.jb")
x_tensor = torch.tensor(final_df_scaled, dtype=torch.float32)
loss_fn = nn.CrossEntropyLoss()
criterion = nn.TripletMarginLoss(margin=1.0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model Class
class TripletNet(nn.Module):
    """Torch Model"""
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

# Triplet Creator
def create_triplets(X, labels):
    """Function for converting dataset and cluster values
    into anchor, positive and negative point"""
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

# Load Model and create triplets
model = TripletNet(final_df_scaled.shape[1]).to(device)
triplets = create_triplets(final_df_scaled, df['cluster'].values)


best_epoch = float('inf')
epochs = 1000

for epoch in range(epochs):

    model.train()
    running_loss = 0.0
    triplet_count = 0

    for anchor, positive, negative in triplets:
        anchor_out = model(x_tensor[anchor])
        positive_out = model(x_tensor[positive])
        negative_out = model(x_tensor[negative])

        loss = (0.5 * loss_fn(anchor_out, negative_out)) + (0.5 * criterion(anchor_out, positive_out, negative_out))
        loss.backward()


        running_loss = loss.item()
        triplet_count += 1

    epoch_loss_train = running_loss/triplet_count

    model.eval()
    running_loss = 0.0
    triplet_count = 0

    with torch.no_grad():
        for anchor, positive, negative in triplets:
            anchor_out = model(x_tensor[anchor])
            positive_out = model(x_tensor[positive])
            negative_out = model(x_tensor[negative])

            loss = (0.5 * loss_fn(anchor_out, negative_out)) + (0.5 * criterion(anchor_out, positive_out, negative_out))

            running_loss = loss.item()
            triplet_count += 1

        epoch_loss_val = running_loss/triplet_count

    print(f"Epoch {epoch+1}")
    print(f"  Train Loss: {epoch_loss_train:.4f}")
    print(f"  Val Loss:   {epoch_loss_val:.4f}")

    if epoch_loss_val < best_epoch:
        best_epoch = epoch_loss_val
        torch.save(model.state_dict(), "_Recommendation System/models/model.mo")