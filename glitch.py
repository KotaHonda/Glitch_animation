import cv2
import numpy as np
import random
import noise

class Glitch():

    def __init__(self, srcImg):
        self.originalImg = srcImg.copy()
        self.editedImg = srcImg.copy()
        self.rows, self.cols, self.channels = srcImg.shape

    def shift_color(self, getImg):
        shift_value = [random.randint(0, 255)], [random.randint(0, 255)], [random.randint(0, 255)]

        for i in range(3):
            getImg[:,:,i] = (getImg[:,:,i] + shift_value[i]) % 256

        return getImg

    def shift_side(self):

        height = random.randint(3, int(self.rows / random.randint(10, 14)))
        pos_y = random.randint(random.randint(int(self.rows / 7), int( 6* self.rows / 7)), self.rows - height)
        shift_size = random.randint(5, int(self.cols / random.randint(1, 5)))
        shift_size *= pow(-1,pos_y % 2)

        shiftImg  = self.editedImg[pos_y : pos_y + height, 0: self.cols]
        affine_mat = np.array([[1.0, 0.0, shift_size], [0.0, 1.0, 0.0]], np.float32)
        shiftImg = cv2.warpAffine(shiftImg, affine_mat, (self.cols, height),borderMode=cv2.BORDER_WRAP)

        self.editedImg[pos_y : pos_y + height, 0: self.cols] = shiftImg

    def enter_line(self):
        pos_y = random.randint(0, self.rows)
        slip_value = [random.randint(1, 255), random.randint(1, 255),random.randint(1, 255)]
        slipImg = self.editedImg[pos_y : pos_y+1, 0: self.cols]

        for i in range(3):
            slipImg[:,:,i] = (slipImg[:,:,i] + slip_value[i]) % 256

        self.editedImg[pos_y : pos_y, 0: self.cols] = slipImg

    def rect_image(self):
        height = random.randint(int(self.rows / 10), int(self.rows / random.randint(5, 9)))
        width = random.randint(int(self.cols / 9), int(self.cols / random.randint(3, 5)))
        pos_y = random.randint(0, self.rows - height)
        pos_x = random.randint(0, self.cols - width)

        rectImg = self.originalImg[pos_y : pos_y + height, pos_x : pos_x + width].copy()

        if random.randint(1, 10) % 10 < 3:
            rectImg = self.shift_color(rectImg)

        pos_y2 = random.randint(0, self.rows - height)
        pos_x2 = random.randint(0, self.cols - width)

        self.editedImg[pos_y2 : pos_y2 + height, pos_x2 : pos_x2 + width] = rectImg

    def get_image(self):

        if random.randint(1, 10) % 10 < 5:
            return self.originalImg
        
        self.editedImg = []
        self.editedImg = self.originalImg.copy()

        if random.randint(1, 15) % 15 < 1:
            self.editedImg = self.shift_color(self.editedImg)

        count = random.randint(4, 13)
        for _ in range(count):
            self.shift_side()
        count = random.randint(5, 18)
        for _ in range(count):
            self.enter_line()
        count = random.randint(0, 4)
        for _ in range(count):
            self.rect_image()

        return self.editedImg
        

if __name__ == '__main__':
    
    srcImg = cv2.imread("sunset.jpg")

    grayImg = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
    resultImg = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2BGR)

    resultImg = noise.add_noise(resultImg, 30)
    resultImg = noise.shift_image(resultImg)

    cv2.imwrite("result.jpg", resultImg)

    srcImg = cv2.imread("result.jpg")

    glitch = Glitch(srcImg)

    IMG_SIZE_h, IMG_SIZE_w, _ = srcImg.shape

    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    video = cv2.VideoWriter('video.mp4', fourcc, 9.0, (IMG_SIZE_w, IMG_SIZE_h))

    for _ in range(270):
        resultImg = glitch.get_image()
        video.write(resultImg)

    video.release()