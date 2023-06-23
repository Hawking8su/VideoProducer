'''
Creating Video from Images using OpenCV-Python
Reference：
1. https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
'''
import cv2
import numpy as np
import glob

img_array = []
for filename in glob.glob('./image/0.jpg'):
    print(filename)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)


out_path = './video/project.avi'
out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'DIVX'), 1, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()


# GET face positions



def get_face_position(in_image_path=""):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(in_image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))
    # return face positions
    return faces

if __name__ =="__main__":
    image_path = r"/Users/liuzuhao/PycharmProjects/VideoProducer/image/windows_people.jpg"
    faces = get_face_position(image_path)
    print(faces)
    for face in faces:
        (x, y, w, h) = face
        x_zoom = int(x + w / 2)
        y_zoom = int(y + h / 2)
        print((x_zoom, y_zoom))

    # (1489, 278)
    # (467, 371)
    # (1074, 580)
