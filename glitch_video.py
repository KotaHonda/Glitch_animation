import cv2
import numpy as np
import random
import noise
import sys

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

    def get_image(self, srcImg, strength):

        self.originalImg = srcImg.copy()

        if random.randint(1, 10) % 10 < 4:
            return self.originalImg
        
        self.editedImg = []
        self.editedImg = self.originalImg.copy()

        if random.randint(1, 21 - 2 * strength) % (21 - 2 * strength) < 1:
            self.editedImg = self.shift_color(self.editedImg)

        count = random.randint(strength, 10 + strength)
        for _ in range(count):
            self.shift_side()
        count = random.randint(2 + strength, 12 + 2 * strength)
        for _ in range(count):
            self.enter_line()
        count = random.randint(max(0, strength - 3), strength)
        for _ in range(count):
            self.rect_image()

        return self.editedImg
        

if __name__ == '__main__':

    strength = 3
    
    if len(sys.argv) > 1:
        strength = int(sys.argv[1])
        
    if strength > 5:
        strength = 5

    capture = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    # grayImg = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
    # resultImg = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2BGR)

    # resultImg = noise.add_noise(resultImg)
    # resultImg = noise.shift_image(resultImg)

    # cv2.imwrite("result.jpg", resultImg)

    # targetImg = cv2.imread("result.jpg")

    ret, srcImg = capture.read()
    IMG_SIZE_h, IMG_SIZE_w, _ = srcImg.shape
    video = cv2.VideoWriter('glitch_video.mp4', fourcc, 9.0, (IMG_SIZE_w, IMG_SIZE_h))
    glitch = Glitch(srcImg)

    while(True):
        ret, srcImg = capture.read()

        
        #grayImg = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
        #grayImg = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2BGR)

        #resultImg = noise.add_noise(grayImg , 5)

        resultImg = noise.shift_image(srcImg)

        resultImg = glitch.get_image(resultImg.astype(np.uint8), strength) 
        cv2.imshow('frame',resultImg)
        video.write(resultImg.astype(np.uint8))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    capture.release()
    cv2.destroyAllWindows()