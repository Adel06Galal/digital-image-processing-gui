import cv2
import numpy as np
import matplotlib.pyplot as plt


def read_image(path, gray=False):
    flag = cv2.IMREAD_GRAYSCALE if gray else cv2.IMREAD_COLOR
    image = cv2.imread(path, flag)

    if image is None:
        raise FileNotFoundError(f"Image not found: {path}")

    return image


def convert_to_gray(image):
    if len(image.shape) == 2:
        return image

    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def resize_second_image(image1, image2):
    height, width = image1.shape[:2]
    return cv2.resize(image2, (width, height))


def limit_values(image):
    return np.clip(image, 0, 255).astype(np.uint8)


def show_histogram(image, title="Image"):
    gray_image = convert_to_gray(image)

    plt.figure(figsize=(7, 4))
    plt.hist(gray_image.ravel(), bins=256, range=(0, 256))
    plt.title(f"{title} Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()
