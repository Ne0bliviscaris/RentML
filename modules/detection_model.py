import torch
from PIL import Image
from torch import nn
from torchvision import transforms

torch.classes.__path__ = []


def build_model():
    """Build a deep learning model to identify the type of a car in an image."""
    model_path = "data/recognition-model/detect_car.pth"
    model = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),  # Convolutional layer
        nn.ReLU(),  # Activation function
        nn.MaxPool2d(kernel_size=2, stride=2),  # Max pooling layer
        nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),  # Another convolutional layer
        nn.ReLU(),  # Activation function
        nn.MaxPool2d(kernel_size=2, stride=2),  # Max pooling layer
        nn.Flatten(),  # Flatten the tensor for the fully connected layer
        nn.Linear(64 * 56 * 56, 128),  # Fully connected layer
        nn.ReLU(),  # Activation function
        nn.Linear(128, 2),  # Output layer
    )
    # Load the trained model
    model.load_state_dict(torch.load(model_path))
    model.eval()  # Set the model to evaluation mode
    return model


def make_prediction(image, model):
    """Make a prediction using the model. Model returns 0 or 1"""
    car_types = {0: "Dostawczy", 1: "Osobowy"}
    # Make a prediction
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, dim=1)
    return car_types[predicted.item()]


def load_image(image):
    """Load an image from a file, and return it as a NumPy array."""
    return Image.open(image).convert("RGB")


def transform_image(image):
    """Transform an image to be compatible with the model."""
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),  # Resize the image
            transforms.ToTensor(),  # Convert the image to a tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize the image
        ]
    )
    return transform(image).unsqueeze(0)


def identify_car(image):
    """Load a trained model and use it to identify the type of a car in an image."""
    model = build_model()
    image = load_image(image)
    transformed_image = transform_image(image)
    return make_prediction(transformed_image, model)
