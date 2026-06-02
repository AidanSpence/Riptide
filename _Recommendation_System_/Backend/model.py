import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import joblib
import random


SAVE_DIR  = "_Recommendation_System_\\models"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model Class
class TripletNet(nn.Module):
    """Torch Model"""
    def __init__(self, input_dim):
        super().__init__()
        self.stack = nn.Sequential(
            nn.Linear(input_dim, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 128))

    def forward(self, x):
        return self.stack(x)

# Triplet Creator
def create_triplets(X, labels, n_samples=10000):
    """Function for converting dataset and cluster values
    into anchor, positive and negative point"""

    label_to_indices = {}
    for i, label in enumerate(labels):
        label_to_indices.setdefault(label, []).append(i)

    indices = list(range(len(X)))
    triplets = []

    n_samples = n_samples or len(X)  # Ensure more than the dataset size isn't sampled

    for _ in range(n_samples):
        anchor = random.choice(indices)
        anchor_label = labels[anchor]

        positive = random.choice(label_to_indices[anchor_label])

        negative_index = random.choice([i for i in label_to_indices.keys() if i != anchor_label])
        negative = random.choice(label_to_indices[negative_index])

        triplets.append((anchor, positive, negative))

    return triplets


def train_model():
    """Function for training the model and saving the best model and embeddings"""
    # Load Model and create triplets
    X = joblib.load(f"{SAVE_DIR}/X_final.jb")
    df = joblib.load(f"{SAVE_DIR}/df.jb")

    X_tensor = torch.tensor(X, dtype=torch.float32).to(DEVICE)

    model = TripletNet(X.shape[1]).to(DEVICE)
    optimizer = optim.SGD(model.parameters(), lr=1e-3)
    criterion = nn.TripletMarginLoss(margin=1.0)


    best_loss = float('inf')
    patience = 0

    labels = df['cluster'].values

    # Training Loop
    for epoch in range(100):
        triplets = create_triplets(X, labels)

        model.train()
        total_loss = 0

        for anchor, positive, negative in triplets:
            anchor_out = model(X_tensor[anchor].unsqueeze(0))
            positive_out = model(X_tensor[positive].unsqueeze(0))
            negative_out = model(X_tensor[negative].unsqueeze(0))

            loss = criterion(anchor_out, positive_out, negative_out)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


            total_loss += loss.item()
        avg_loss = total_loss / len(triplets)

        print(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}")

        if avg_loss < best_loss:
            best_loss = avg_loss
            patience = 0

            with torch.no_grad():
                embeddings = model(X_tensor).detach().cpu().numpy()

            torch.save(model.state_dict(), f"{SAVE_DIR}/model.pt")
            np.savez_compressed(f"{SAVE_DIR}/embeddings.npz", embeddings=embeddings)

        else:
            patience += 1
            if patience >= 10:
                print("Early stop")
                break

if __name__ == "__main__":
    train_model()
    print("Model training complete and saved.")