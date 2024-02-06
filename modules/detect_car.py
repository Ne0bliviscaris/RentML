# v1.01 - car identification using deep learning model
import os

import torch
from PIL import Image
from torch import nn
from torchvision import transforms


# def identify(img_path, model_path="..\data\recognition-modeldetect_car.pth")
def identify(img_path, model_path=None):
    if model_path is None:
        model_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "recognition-model",
            "detect_car.pth",
        )
    """
    Load a trained model and use it to identify the type of a car in an image.

    Args:
        img_path (str): The path to the image of the car.

    Returns:
        str: The identified type of the car ('truck' or 'car').
    """
    # Define the model architecture
    model = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),  # Convolutional layer
        nn.ReLU(),  # Activation function
        nn.MaxPool2d(kernel_size=2, stride=2),  # Max pooling layer
        nn.Conv2d(
            32, 64, kernel_size=3, stride=1, padding=1
        ),  # Another convolutional layer
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

    # Define the image transformations
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),  # Resize the image
            transforms.ToTensor(),  # Convert the image to a tensor
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),  # Normalize the image
        ]
    )

    # Load and transform the image
    image = Image.open(img_path).convert("RGB")
    if transform:
        image = transform(image)

    # Add a batch dimension
    image = image.unsqueeze(0)

    # Define the class names
    class_names = {0: "truck", 1: "car"}

    # Make a prediction
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, dim=1)

    # Return the predicted class
    return class_names[predicted.item()]


# Test the function with an image
# print(identify("dataset/ml_test/20230818_164327.jpg"))
