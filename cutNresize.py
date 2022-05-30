import cv2
import os
from glob import glob

WIDTH = 224
HEIGHT = 224


def cutNresize(src, dst):
    file_list = [[], []]
    cascade_file = "lbpcascade_animeface.xml"
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    files = [y for x in os.walk(src) for y in glob(os.path.join(x[0], '*.*'))]
    for image_file in files:
        target_path = "/".join(image_file.strip("/").split('/')[1:-1])
        target_path = os.path.join(dst, target_path) + "/"
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        image = cv2.imread(image_file, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor=1.1,
                                         minNeighbors=3,
                                         minSize=(30, 30))
        i = 0
        for (x, y, w, h) in faces:
            crop_img = image[y:y + h, x:x + w]
            resized_image = cv2.resize(crop_img, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
            filename = os.path.splitext(os.path.basename(image_file))[0]
            cv2.imwrite(
                os.path.join(target_path, filename + str(i) + ".jpg"),
                resized_image
            )
            file_list[0].append(os.path.join(image_file))
            file_list[1].append(os.path.join(target_path + filename + str(i) + ".jpg"))
            i += 1

    return file_list
