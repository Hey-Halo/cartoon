"""A module containing the cartoonize function"""
import cv2 as cv


def cartoonize(image, item):
    """A function that transforms an image into a cartoonized form"""

    if item == "Type 1":
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (3, 3), 1)
        edges = cv.Laplacian(gray, -1, ksize=5)
        edges = 255 - edges

        ret, edges = cv.threshold(edges, 150, 255, cv.THRESH_BINARY)

        edgePreservingImage = cv.edgePreservingFilter(
            image, flags=2, sigma_s=150, sigma_r=0.6)

        return cv.bitwise_and(edgePreservingImage,
                              edgePreservingImage, mask=edges)

    if item == "Type 2":
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray = cv.medianBlur(gray, 7)
        edges = cv.adaptiveThreshold(
            gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 6)

        color = cv.bilateralFilter(image, 12, 250, 250)
        return cv.bitwise_and(color, color, mask=edges)

    if item == "Type 3":
        return cv.stylization(image, sigma_s=150, sigma_r=0.25)

    if item == "Pencil sketch 1":
        cartoonImage1, cartoonImage2 = cv.pencilSketch(
            image, sigma_s=150, sigma_r=0.2, shade_factor=0.015)
        return cartoonImage1

    cartoonImage1, cartoonImage2 = cv.pencilSketch(
        image, sigma_s=150, sigma_r=0.2, shade_factor=0.015)
    return cartoonImage2
