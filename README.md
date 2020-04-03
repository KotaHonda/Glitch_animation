# Glitch_animation

## operating environment  
```
(input) $ python -V
(output)$ Python 3.6.8

(input) $ pip install numpy=1.15.4, opencv-python
```

## glitch.py - create glitch image

this glitch.py turns the input image into a corrupted image and a corrupted video.    
### input image  
![sunset](https://user-images.githubusercontent.com/55595081/78325182-e3384b80-75b1-11ea-9e16-e78a97991de9.jpg) 
### output image  
![result](https://user-images.githubusercontent.com/55595081/78325184-e6333c00-75b1-11ea-936e-737ec1e760ef.jpg)
### output video
Please download video.mp4 and watch it  

### run program
```
$ python glitch.py image.jpg
```  
Please replace this image.jpg with the file path of your favorite image  
If not specified, sunset.jpg will be executed  

## glitch_video.py - create glitch animation from image

glitch_video.py converts the camera image to a damaged image and outputs (displays) it.　

### run program  
```
$ python glitch_video.py 3
```  
The argument (3) is the damage strength, which can be specified from 0 to 5.
If not specified, the program will be executed with the default value of 3.

