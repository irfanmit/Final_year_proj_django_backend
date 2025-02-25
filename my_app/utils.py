import torch
from ultralytics.nn.tasks import DetectionModel  # Import the class causing the error

# Allowlist the DetectionModel class
torch.serialization.add_safe_globals([DetectionModel])

def load_model(model_path):
    """
    Load the PyTorch model from the given path.
    """
    # Use weights_only=True with the allowlisted class
    model = torch.load(
    "tensors.pt", map_location=lambda storage, loc: storage, weights_only=True
)
    model.eval()
    return model