import cv2
import numpy as np
from collections import Counter

from image_tools import convert_to_gray, resize_second_image, limit_values


def ensure_color(image): 
    if len(image.shape) == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) 
    return image


def add_images(image1, image2):
    image2 = resize_second_image(image1, image2)
    return cv2.add(image1, image2)


def subtract_images(image1, image2):
    image2 = resize_second_image(image1, image2)
    return cv2.subtract(image1, image2)


def divide_images(image1, image2):
    image2 = resize_second_image(image1, image2)
    safe_image2 = np.where(image2 == 0, 1, image2)

    result = (image1.astype(np.float32) / safe_image2.astype(np.float32)) * 255
    return limit_values(result)


def complement_image(image):
    return 255 - image


def change_red_channel(image, value=60):
    image = ensure_color(image)

    result = image.copy().astype(np.int16)
    result[:, :, 2] += value

    return limit_values(result)


def swap_red_green(image):
    image = ensure_color(image)

    result = image.copy()
    result[:, :, [1, 2]] = result[:, :, [2, 1]]

    return result


def eliminate_red_channel(image):
    image = ensure_color(image)

    result = image.copy()
    result[:, :, 2] = 0

    return result


def histogram_stretching(image):
    gray_image = convert_to_gray(image)

    minimum = np.min(gray_image)
    maximum = np.max(gray_image)

    if maximum == minimum:
        return gray_image.copy()

    result = (gray_image - minimum) * (255.0 / (maximum - minimum))
    return limit_values(result)


def histogram_equalization(image):
    gray_image = convert_to_gray(image)
    return cv2.equalizeHist(gray_image)


def average_filter(image, kernel_size=3):
    return cv2.blur(image, (kernel_size, kernel_size))


def laplacian_filter(image):
    gray_image = convert_to_gray(image)
    result = cv2.Laplacian(gray_image, cv2.CV_64F)

    return limit_values(np.abs(result))


def maximum_filter(image, kernel_size=3):
    kernel = create_kernel(kernel_size)
    return cv2.dilate(image, kernel)


def minimum_filter(image, kernel_size=3):
    kernel = create_kernel(kernel_size)
    return cv2.erode(image, kernel)


def median_filter(image, kernel_size=3):
    return cv2.medianBlur(image, kernel_size)


def mode_filter(image, kernel_size=3):
    gray_image = convert_to_gray(image)
    padding = kernel_size // 2

    padded_image = cv2.copyMakeBorder(
        gray_image,
        padding,
        padding,
        padding,
        padding,
        cv2.BORDER_REPLICATE
    )

    result = np.zeros_like(gray_image)

    for row in range(gray_image.shape[0]):
        for col in range(gray_image.shape[1]):
            window = padded_image[row:row + kernel_size, col:col + kernel_size].flatten()
            result[row, col] = Counter(window).most_common(1)[0][0]

    return result


def add_salt_pepper_noise(image, salt=0.02, pepper=0.02):
    result = image.copy()
    random_values = np.random.random(image.shape[:2])

    salt_pixels = random_values > 1 - salt
    pepper_pixels = random_values < pepper

    if len(image.shape) == 2:
        result[pepper_pixels] = 0
        result[salt_pixels] = 255
    else:
        result[pepper_pixels] = [0, 0, 0]
        result[salt_pixels] = [255, 255, 255]

    return result


def salt_pepper_average_filter(image, kernel_size=3):
    return average_filter(image, kernel_size)


def salt_pepper_median_filter(image, kernel_size=3):
    return median_filter(image, kernel_size)


def salt_pepper_outlier_method(image, threshold=40, kernel_size=3):
    median_image = cv2.medianBlur(image, kernel_size)
    difference = cv2.absdiff(image, median_image)

    if len(image.shape) == 3:
        difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

    mask = difference > threshold

    result = image.copy()
    result[mask] = median_image[mask]

    return result


def add_gaussian_noise(image, mean=0, sigma=25):
    noise = np.random.normal(mean, sigma, image.shape)
    result = image.astype(np.float32) + noise

    return limit_values(result)


def image_averaging(images):
    if not images:
        raise ValueError("Images list is empty.")

    base_image = images[0]
    result = np.zeros_like(base_image, dtype=np.float32)

    for image in images:
        if image.shape != base_image.shape:
            image = cv2.resize(image, (base_image.shape[1], base_image.shape[0]))

        result += image.astype(np.float32)

    result /= len(images)
    return limit_values(result)


def gaussian_average_filter(image, kernel_size=3):
    return average_filter(image, kernel_size)


def basic_global_thresholding(image, threshold=127):
    gray_image = convert_to_gray(image)

    _, result = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    return result


def automatic_thresholding(image):
    gray_image = convert_to_gray(image)

    _, result = cv2.threshold(
        gray_image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return result


def adaptive_thresholding(image, block_size=11, c=2):
    gray_image = convert_to_gray(image)

    if block_size % 2 == 0:
        block_size += 1

    return cv2.adaptiveThreshold(
        gray_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size,
        c
    )


def sobel_detector(image):
    gray_image = convert_to_gray(image)

    sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

    result = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
    return limit_values(result)


def create_kernel(kernel_size=3):
    return np.ones((kernel_size, kernel_size), np.uint8)


def make_binary(image, threshold=127):
    gray_image = convert_to_gray(image)

    _, result = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    return result


def image_dilation(image, kernel_size=3):
    binary_image = make_binary(image)
    kernel = create_kernel(kernel_size)

    return cv2.dilate(binary_image, kernel)


def image_erosion(image, kernel_size=3):
    binary_image = make_binary(image)
    kernel = create_kernel(kernel_size)

    return cv2.erode(binary_image, kernel)


def image_opening(image, kernel_size=3):
    binary_image = make_binary(image)
    kernel = create_kernel(kernel_size)

    return cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)


def internal_boundary(image, kernel_size=3):
    binary_image = make_binary(image)
    eroded_image = cv2.erode(binary_image, create_kernel(kernel_size))

    return cv2.subtract(binary_image, eroded_image)


def external_boundary(image, kernel_size=3):
    binary_image = make_binary(image)
    dilated_image = cv2.dilate(binary_image, create_kernel(kernel_size))

    return cv2.subtract(dilated_image, binary_image)
 
def morphological_gradient(image, kernel_size=3):
    binary_image = make_binary(image)
    kernel = create_kernel(kernel_size)

    return cv2.morphologyEx(binary_image, cv2.MORPH_GRADIENT, kernel)
