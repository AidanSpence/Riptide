from pathlib import Path
import random
import joblib
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent
SAVE_DIR = PROJECT_ROOT / "_Recommendation_System_" / "models"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TripletNet(nn.Module):
    """Deep Neural Network for learning low-dimensional vector embeddings."""
    def __init__(self, input_dim: int):
        super().__init__()
        self.stack = nn.Sequential(
            nn.Linear(input_dim, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 128))

    def forward(self, x: torch.Tensor):
        return self.stack(x)


def create_triplets(labels: np.ndarray, n_samples: int = 10000):
    """Generates anchor, positive and negative point from dataset and cluster values"""

    label_to_indices = {}
    for i, label in enumerate(labels):
        label_to_indices.setdefault(label, []).append(i)

    all_labels = list(label_to_indices.keys())
    all_indices = list(range(len(labels)))

    anchors, positives, negatives = [], [], []

    for _ in range(n_samples):
        anchor = random.choice(all_indices)
        anchor_label = labels[anchor]

        positive = random.choice(label_to_indices[anchor_label])

        negative_label = random.choice([label for label in label_to_indices.keys() if label != anchor_label])
        negative = random.choice(label_to_indices[negative_label])
        
        anchors.append(anchor)
        positives.append(positive)
        negatives.append(negative)

    return anchors, positives, negatives


def train_model():
    """Trains the embedding model using optimized batch triplet ranking loss and saves the best model and embeddings"""

    # Load Model and create triplets
    X = joblib.load(SAVE_DIR / "X_final.jb")
    df = joblib.load(SAVE_DIR / "df.jb")
    labels = df['cluster'].values

    X_tensor = torch.tensor(X, dtype=torch.float32).to(DEVICE)

    model = TripletNet(X.shape[1]).to(DEVICE)
    optimizer = optim.SGD(model.parameters(), lr=1e-3)
    criterion = nn.TripletMarginLoss(margin=1.0)

    best_loss = float('inf')
    patience_counter = 0

    labels = df['cluster'].values

    # Training Loop
    for epoch in range(100):
        triplets = create_triplets(X, labels)

        model.train()

        # Extract indices 
        anc_idx, pos_idx, neg_idx = create_triplets(labels, n_samples=10000)

        # Send directly to GPU/CPU at same time
        anchor_out = model(X_tensor[anc_idx])
        positive_out = model(X_tensor[pos_idx])
        negative_out = model(X_tensor[neg_idx])

        loss = criterion(anchor_out, positive_out, negative_out)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        avg_loss = total_loss / len(triplets)
        print(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}")

        # Early Stopping Check
        if avg_loss < best_loss:
            best_loss = avg_loss
            patience_counter = 0

            # Export updated embeddings
            with torch.no_grad():
                embeddings = model(X_tensor).detach().cpu().numpy()

            torch.save(model.state_dict(), SAVE_DIR / "model.pt")
            np.savez_compressed(SAVE_DIR / "embeddings.npz", embeddings=embeddings)
        else:
            patience_counter += 1
            if patience_counter >= 10:
                print("Early stop")
                break

if __name__ == "__main__":
    train_model()
    print("Model training complete and saved.")