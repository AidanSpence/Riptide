import joblib
import random
import torch
from torch import optim
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

save_dir = "_Recommendation_System_\models"

# Load necessary variables and check device
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("Number of GPUs:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

final_df_scaled = joblib.load("_Recommendation System_/models/final_df_scaled.jb")

df = joblib.load("_Recommendation System_/models/df.jb")

x_tensor = torch.tensor(final_df_scaled, dtype=torch.float32).to(device)

criterion = nn.TripletMarginLoss(margin=1.0)

print(device)
print("Shape:", final_df_scaled.shape)
print("Min:", np.min(final_df_scaled))
print("Max:", np.max(final_df_scaled))
print("Mean:", np.mean(final_df_scaled))
print("Std:", np.std(final_df_scaled))

# Model Class
class TripletNet(nn.Module):
    """Torch Model"""
    def __init__(self, input_dim):
        super(TripletNet, self).__init__()
        self.stack = nn.Sequential(
            nn.Linear(input_dim, 1024),
            nn.ReLU(),
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Linear(1024, 128))

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
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

best_epoch = float('inf')
patience_counter = 0
epochs = 100

# Training Loop
for epoch in range(epochs):

    model.train()
    running_loss = 0.0
    triplet_count = 0

    for anchor, positive, negative in triplets:
        anchor_out = model(x_tensor[anchor].unsqueeze(0))
        positive_out = model(x_tensor[positive].unsqueeze(0))
        negative_out = model(x_tensor[negative].unsqueeze(0))

        loss = criterion(anchor_out, positive_out, negative_out)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


        running_loss += loss.item()
        triplet_count += 1

    epoch_loss_train = running_loss/triplet_count

    model.eval()
    running_loss = 0.0
    triplet_count = 0

    # Validation Loop
    with torch.no_grad():
        for anchor, positive, negative in triplets:
            anchor_out = model(x_tensor[anchor].unsqueeze(0))
            positive_out = model(x_tensor[positive].unsqueeze(0))
            negative_out = model(x_tensor[negative].unsqueeze(0))

            loss = criterion(anchor_out, positive_out, negative_out)

            running_loss += loss.item()

            triplet_count += 1

        epoch_loss_val = running_loss/triplet_count

    print(f"Epoch {epoch+1}")
    print(f"  Train Loss: {epoch_loss_train:.4f}")
    print(f"  Val Loss:   {epoch_loss_val:.4f}")

    if epoch_loss_val < best_val_loss:
        best_val_loss = epoch_loss_val
        patience_counter = 0

        with torch.no_grad():
            embeddings = model(x_tensor)

        torch.save(model.state_dict(), f"{save_dir}/model.pt")
        np.save(f"{save_dir}/embeddings.npy", embeddings)

    else:
        patience_counter += 1
        if patience_counter >= 10:
            print("Early stop")
            break