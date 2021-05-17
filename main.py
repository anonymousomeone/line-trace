import os
import cv2
import numpy as np


def videotomp3():
    os.system('ffmpeg -i ./input/badapple.mp4 ./mp3/audio.mp3')


def mp3combinevideo():
    os.system('ffmpeg -y -i ./mp3/audio.mp3 -r 30 -i ./intermediate3/movie.mp4 ./output/final.mp4')


def vidtojpg():
    vidcap = cv2.VideoCapture('./input/badapple.mp4')
    success, image = vidcap.read()
    count = 1
    while success:
        cv2.imwrite("./intermediate1/frame_%d.jpg" % count, image)
        success, image = vidcap.read()
        print('Saved image ', count)
        count += 1


def create_line_drawing_image(img):
    kernel = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        ], np.uint8)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_dilated = cv2.dilate(img_gray, kernel, iterations=1)
    img_diff = cv2.absdiff(img_dilated, img_gray)
    contour = 255 - img_diff
    return contour


def imagetovideo():
    os.system('ffmpeg -r 30 -i intermediate2/frame_%01d.jpg -vcodec mpeg4 -y intermediate3/movie.mp4')


def convert_images(dir_from, dir_to):
    for file_name in os.listdir(dir_from):
        if file_name.endswith('.jpg'):
            print(file_name)
            img = cv2.imread(os.path.join(dir_from, file_name))
            img_contour = create_line_drawing_image(img)
            cv2.imwrite(os.path.join(dir_to, file_name), img_contour)


videotomp3()
vidtojpg()
convert_images('./intermediate1', './intermediate2')
imagetovideo()
mp3combinevideo()

