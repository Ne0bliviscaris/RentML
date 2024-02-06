# v1.0
import cv2
import matplotlib.pyplot as plt
import numpy as np


# 2. ORDER: 1. GAMMA CORRECTION, 2. EROSION, 3. EDGE DETECTION 4. SHARPENING
def unsharp_mask(
    image: np.ndarray, sigma: float = 16.0, strength: float = 4.5
) -> np.ndarray:
    """
    Apply unsharp mask to the image to enhance the details.

    Args:
        image (np.ndarray): The original image.
        sigma (float, optional): The standard deviation for the Gaussian kernel. Defaults to 16.0.
        strength (float, optional): The amount of details to enhance. Defaults to 4.5.

    Returns:
        np.ndarray: The image with enhanced details.
    """
    # Gaussian blur of the image
    blurred = cv2.GaussianBlur(image, (1, 1), sigma)
    # Enhance the image by adding a weighted difference between the original image and the blurred one
    sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
    return sharpened


def adjust_gamma(image: np.ndarray, gamma: float = 1.2) -> np.ndarray:
    """
    Adjust the gamma of the image.

    Args:
        image (np.ndarray): The original image.
        gamma (float, optional): The gamma value to adjust the image. Defaults to 1.2.

    Returns:
        np.ndarray: The image with adjusted gamma.
    """
    # Build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    invGamma = 5 / gamma
    table = np.array(
        [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]
    ).astype("uint8")

    # Apply gamma correction for the image
    return cv2.LUT(image, table)


def edge_detection(img: np.ndarray) -> np.ndarray:
    """
    Apply edge detection to the image.

    Args:
        img (np.ndarray): The original image.

    Returns:
        np.ndarray: The image with detected edges.
    """
    # Apply Gaussian blur to reduce noise
    img_blur = cv2.GaussianBlur(img, (29, 29), 1)

    # Apply Canny edge detection
    edges = cv2.Canny(img_blur, 50, 90)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    img_with_contours = cv2.drawContours(img.copy(), contours, -3, (0, 255, 0), 2)

    # Display the image with contours using matplotlib
    # plt.imshow(img_with_contours, cmap='gray')
    # plt.show()
    return img_with_contours


def preprocess(img: np.ndarray) -> np.ndarray:
    """
    Preprocesses an image for further analysis.

    The function takes an image as a numpy array, converts the color from BGR to RGB, adjusts the gamma, applies erosion, detects edges, and applies an unsharp mask for sharpening.

    Args:
        img (np.ndarray): The image to be preprocessed.

    Returns:
        np.ndarray: The preprocessed image as a numpy array.
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gamma_corrected_img = adjust_gamma(
        img, gamma=1.2
    )  # You can adjust the gamma value depending on your image
    kernel = np.ones((3, 3), np.uint8)
    eroded_img = cv2.erode(gamma_corrected_img, kernel, iterations=4)
    edge_img = edge_detection(eroded_img)
    sharpened_img = unsharp_mask(edge_img)

    print("Original image:")
    plt.imshow(img, cmap="gray")
    plt.show()
    # print("Gamma corrected image:") # Uncomment to display the gamma corrected image
    # plt.imshow(gamma_corrected_img, cmap='gray') # Uncomment to display the gamma corrected image
    # plt.show() # Uncomment to display the gamma corrected image
    # print("Eroded image:") # Uncomment to display the eroded image
    # plt.imshow(eroded_img, cmap='gray') # Uncomment to display the eroded image
    # plt.show() # Uncomment to display the eroded image
    # print("Edge detected image:") # Uncomment to display the edge detected image
    # plt.imshow(edge_img, cmap='gray') # Uncomment to display the edge detected image
    # plt.show() # Uncomment to display the edge detected image
    print("Sharpened image:")
    plt.imshow(sharpened_img, cmap="gray")
    plt.show()

    return sharpened_img
