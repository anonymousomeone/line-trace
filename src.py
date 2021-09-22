import os
import cv2
import numpy as np
from tinytag import TinyTag

kernel = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        ], np.uint8)


def create_line_drawing_image(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_dilated = cv2.dilate(img_gray, kernel, iterations=1)
    img_diff = cv2.absdiff(img_dilated, img_gray)
    contour = 255 - img_diff
    return contour


def main():
    file = os.listdir('./input')
    files = []
    for thing in file:
        files.append(thing)
    file = files[0]
    video = TinyTag.get('./input/' + file)
    bitrate = str(video.bitrate)
    os.system('ffmpeg -i ./input/' + file + ' ./mp3/audio.mp3')
    print('Converting...')
    vidcap = cv2.VideoCapture('./input/' + file)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    fps = str(fps)
    success, image = vidcap.read()
    count = 1
    while success:
        img_contour = create_line_drawing_image(image)
        success, image = vidcap.read()
        cv2.imwrite("./intermediate1/frame_%d.jpg" % count, img_contour)
        count += 1
    print('Done')
    os.system('ffmpeg -r ' + fps + ' -i intermediate1/frame_%01d.jpg -vcodec mpeg4 -y  -b:v ' + bitrate + 'k intermediate2/movie.mp4 ')
    os.system('ffmpeg -y -i ./mp3/audio.mp3 -r ' + fps + ' -i ./intermediate2/movie.mp4 ./output/' + file)
    files = os.scandir('./intermediate1')
    for f in files:
        os.remove(f)
    files = os.scandir('./intermediate2')
    for f in files:
        os.remove(f)
    files = os.scandir('./mp3')
    for f in files:
        os.remove(f)


main()
