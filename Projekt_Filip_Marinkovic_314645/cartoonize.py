import cv2 as cv
import numpy as np


def cartoonize(image):
    """A function that transforms an image into a cartoonized form"""

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (3, 3), 1)
    edges = cv.Laplacian(gray, -1, ksize=5)
    edges = 255 - edges

    # cv.imshow("edges1", edges)

    ret, edges = cv.threshold(edges, 150, 255, cv.THRESH_BINARY)

    # cv.imshow("edges2", edges)

    edgePreservingImage = cv.edgePreservingFilter(
        image, flags=2, sigma_s=150, sigma_r=0.6)

    # cv.imshow("edgePreservingImage", edgePreservingImage)

    return cv.bitwise_and(edgePreservingImage,
                          edgePreservingImage, mask=edges)
