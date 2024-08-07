import cv2
import numpy as np
import matplotlib.pyplot as plt
def brightness_difference():
    gray_image_6 = cv2.imread('6.bmp', cv2.IMREAD_GRAYSCALE )
    gray_image_7 = cv2.imread('7.bmp', cv2.IMREAD_GRAYSCALE)
    gray_image_8 = cv2.imread('8.bmp', cv2.IMREAD_GRAYSCALE)
    gray_image_9 = cv2.imread('9.bmp', cv2.IMREAD_GRAYSCALE)
    gray_image_0 = cv2.imread('0.bmp', cv2.IMREAD_GRAYSCALE)

    image_output = (gray_image_8-gray_image_6-gray_image_0)
    image_output_1 =(gray_image_9-gray_image_7-gray_image_0)
    return image_output,image_output_1
#对image_output求反正切
def phase_settlement(image_output,image_output_1):
    image=np.arctan2(image_output,image_output_1)
    i=0
    while i<2048:
        j=0
        while j<2560:
            if image[i,j]<=0:
                image[i, j] += 2*np.pi
            j+=1
        i+=1

    return image
if __name__ == '__main__':
    image_output, image_output_1= brightness_difference()
    image=phase_settlement(image_output,image_output_1)
    plt.imshow(image)
    plt.show()

