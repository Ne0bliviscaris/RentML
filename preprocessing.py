import cv2

# from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


# 2. ORDER: 1. GAMMA CORRECTION, 2. EROSION, 3. EDGE DETECTION 4. SHARPENING
def unsharp_mask(image, sigma=16.0, strength=4.5):
    # Rozmycie Gaussowskie obrazu
    blurred = cv2.GaussianBlur(image, (1, 1), sigma)
    # Wzmacniamy obraz poprzez dodanie ważonej różnicy między oryginalnym obrazem a rozmytym
    sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
    return sharpened


def adjust_gamma(image, gamma=1.2):
    # Budujemy tablicę do mapowania każdej skali szarości na jej odpowiednik po korekcji gamma
    invGamma = 5 / gamma
    table = np.array(
        [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]
    ).astype("uint8")

    # Zastosuj mapowanie gamma do obrazu wejściowego
    return cv2.LUT(image, table)


def edge_detection(img):
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


def preprocess(img):
    """
    Preprocesses an image for further analysis.

    The function reads an image from the file path provided, checks if the image is loaded properly, and resizes the image to a maximum dimension of 1080 pixels, maintaining the aspect ratio.

    Args:
        file (str): The file path to the image to be preprocessed.

    Returns:
        numpy.ndarray or None: The preprocessed image as a numpy array if the image is loaded properly, or None if the image cannot be read.
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gamma_corrected_img = adjust_gamma(
        img, gamma=1.2
    )  # Możesz dostosować wartość gamma w zależności od Twojego obrazu
    kernel = np.ones((3, 3), np.uint8)
    eroded_img = cv2.erode(gamma_corrected_img, kernel, iterations=4)
    edge_img = edge_detection(eroded_img)
    sharpened_img = unsharp_mask(edge_img)

    print("Original image:")
    plt.imshow(img, cmap="gray")
    plt.show()
    # print("Gamma corrected image:")
    # plt.imshow(gamma_corrected_img, cmap='gray')
    # plt.show()
    # print("Eroded image:")
    # plt.imshow(eroded_img, cmap='gray')
    # plt.show()
    # print("Edge detected image:")
    # plt.imshow(edge_img, cmap='gray')
    # plt.show()
    print("Sharpened image:")
    plt.imshow(sharpened_img, cmap="gray")
    plt.show()

    return sharpened_img


#
