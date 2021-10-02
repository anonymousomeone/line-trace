import os
import cv2
import numpy as np
from tinytag import TinyTag
from pytube import YouTube
import json
import sys
import progressbar

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


def linetracevideo(inpt, output, directory):
    video = TinyTag.get(inpt)
    bitrate = str(video.bitrate)

    print('Separating audio...')
    os.system('ffmpeg -loglevel panic -i ' + inpt + ' ' + directory + 'mp3/audio.mp3')
    print('Done\n')

    print('Converting to linetraced images...')
    vidcap = cv2.VideoCapture(inpt)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    fps = str(fps)
    success, image = vidcap.read()
    count = 1
    while success:
        img_contour = create_line_drawing_image(image)
        success, image = vidcap.read()
        cv2.imwrite(directory + "intermediate1/frame_%d.jpg" % count, img_contour)
        count += 1
    print('Done\n')

    print('Combining images...')
    os.system('ffmpeg -loglevel panic -r ' + fps + ' -i ' + directory +
              'intermediate1/frame_%01d.jpg -vcodec mpeg4 -y  -b:v ' + bitrate + 'k ' + directory +
              'intermediate2/movie.mp4 ')
    print('Done\n')

    print('Adding audio...')
    os.system('ffmpeg -loglevel panic -y -i ' + directory + 'mp3/audio.mp3 -r ' + fps + ' -i ' + directory +
              'intermediate2/movie.mp4 ' + output)
    print('Done\n')

    files = os.scandir(directory + 'intermediate1')
    for f in files:
        os.remove(f)
    files = os.scandir(directory + 'intermediate2')
    for f in files:
        os.remove(f)
    files = os.scandir(directory + 'mp3')
    for f in files:
        os.remove(f)
    main()


def linetraceimage(inpt, output):
    print('Linetracing image...')
    image = cv2.imread(inpt)
    img_contour = create_line_drawing_image(image)
    cv2.imwrite(output, img_contour)
    print('Done')
    main()


def linetrace():
    filelist = os.listdir('./input')
    midlist = ['back']
    for f in filelist:
        if ".mp4" in f or '.png' in f or '.jpg' in f or '.jpeg' in f:
            midlist.append(f)
    print("Press letter of item to linetrace OR type name of item")
    for i in range(len(midlist)):
        print(i, ":", midlist[i])

    choice = input()
    if int(choice) == 0:
        main()
    if len(choice) > 2:
        results = []
        print('\n' * 20)
        print('RESULTS FOR: ' + choice)
        for item in midlist:
            if choice.lower() in item.lower()[:-4]:
                results.append(item)
        print("Press letter of item to linetrace")
        for i in range(len(results)):
            print(i, ":", results[i])
        choice = input()
        file = ('./input/' + results[int(choice)])
        output = ('./output/' + results[int(choice)])
        directory = './'
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            linetraceimage(file, output)
        else:
            linetracevideo(file, output, directory)
    else:
        file = ('./input/' + midlist[int(choice)])
        output = ('./output/' + midlist[int(choice)])
        directory = './'
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            linetraceimage(file, output)
        else:
            linetracevideo(file, output, directory)


def progress(x, original):
    percent = (original - x) / original * 100
    bar = '['
    for i in range(int(percent)):
        bar += '='
    for i in range(int(100 - percent)):
        bar += '-'
    bar += ']'

    sys.stdout.write('\r')
    sys.stdout.write(bar + ' ' + str(int(percent)) + '%')
    sys.stdout.flush()


original = 0


def progress_func(a, b, c):
    global original
    if not progress_func.has_been_called:
        original = int(c)
    progress(int(c), original)
    progress_func.has_been_called = True


progress_func.has_been_called = False


def ytdl():
    link = input('Link: ')
    midlist = ['mp4', 'mp3']
    print("Press number of filetype to download")
    for i in range(len(midlist)):
        print(i, ":", midlist[i])
    extension = 'mp4'
    try:
        choice = int(input())
        if choice == 0:
            extension = 'mp4'
        elif choice == 1:
            extension = 'mp3'
        else:
            print("That isnt a choice!")
            ytdl()
    except:
        print('That isnt a number!')
        ytdl()
    try:
        yt = YouTube(link,
                     on_progress_callback=progress_func,
                     )
        if yt.age_restricted:
            yt = YouTube(
                link,
                use_oauth=True,
                allow_oauth_cache=True,
                on_progress_callback=progress_func,
            )
    except:
        raise Exception('Error downloading!')
    print('Title: ' + yt.title + '\nLength: ' + str(yt.length))
    download_folder = os.path.expanduser("~") + "/Downloads/"
    print('Downloading...')
    global ran
    ran = False
    yt.streams.filter(progressive=True, file_extension=extension).order_by('resolution').first().download(download_folder)
    print('\nSaved to: ' + download_folder)
    main()


def config():
    pass


def main():
    midlist = ['exit', 'config', 'ytdl', 'linetrace']
    print("Press number of tool to use")
    for i in range(len(midlist)):
        print(i, ":", midlist[i])
    kill = False
    try:
        choice = int(input())
        if choice == 0:
            kill = True
            exit(0)
        elif choice == 1:
            config()
        elif choice == 2:
            ytdl()
        elif choice == 3:
            linetrace()
        else:
            print('Not a choice!')
            main()
     except:
         if kill:
             exit(0)
         print('That isnt a number!')
         main()


if __name__ == '__main__':
    main()
