import cv2
import numpy as np
import random

def add_noise(srcImg, noise_num):
    shapes = srcImg.shape

    noise = np.random.normal(0, noise_num, shapes)
    noise = noise.reshape(shapes)

    noiseImg = noise + srcImg.copy()

    return noiseImg

def shift_image(srcImg):
    shapes = srcImg.shape
    rows, cols = shapes[:2]
    affine_r = np.array([[1.0, 0.0, 4.0], [0.0, 1.0, 5.0]], np.float32)
    affine_g = np.array([[1.0, 0.0, -4.0], [0.0, 1.0, -5.0]], np.float32)

    #blue = srcImg[:,:,0]
    blue = cv2.warpAffine(srcImg[:,:,0], affine_g, (cols, rows),borderMode=cv2.BORDER_WRAP)
    green = cv2.warpAffine(srcImg[:,:,1], affine_g, (cols, rows),borderMode=cv2.BORDER_WRAP)
    #green = srcImg[:,:,1]
    red = cv2.warpAffine(srcImg[:,:,2], affine_r, (cols, rows),borderMode=cv2.BORDER_WRAP)

    return cv2.merge((blue, green, red))

def dust(srcImg):
    returnImg = srcImg.copy()
    rows, cols = srcImg.shape[:2]
    mouse = srcImg[ int(5 * rows / 8) : int(6 * rows / 8), int(cols / 4) : int(5 * cols / 8) ].copy()
    right_eye = srcImg[ int(3 * rows / 8) : int(4 * rows / 8), int(cols / 2) : int(6 * cols / 8) ]

    shift_value_mouse = [random.randint(-32, 128)], [random.randint(-32, 128)], [random.randint(-32, 128)]
    shift_value_eye = [random.randint(0, 128)], [random.randint(0, 128)], [random.randint(0, 128)]

    for i in range(3):
        mouse[:,:,i] = (mouse[:,:,i] + shift_value_mouse[i])
        right_eye[:,:,i] = (right_eye[:,:,i] + shift_value_eye[i])

    returnImg[ int(5 * rows / 8) : int(6 * rows / 8), int(cols / 4) : int(5 * cols / 8) ] = mouse
    returnImg[ int(3 * rows / 8) : int(4 * rows / 8), int(cols / 2) : int(6 * cols / 8) ] = right_eye

    return returnImg


if __name__ == '__main__':
    srcPath = "face.jpg"
    srcImg = cv2.imread(srcPath)

    grayImg = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
    grayImg = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2BGR)

    resultImg = add_noise(grayImg, 30)

    resultImg = shift_image(resultImg)

    resultImg = dust(resultImg)

    print(type(resultImg[0,0,0]))

    cv2.imwrite("./result2.jpg", resultImg)