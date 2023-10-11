import tkinter as tk
from tkinter import filedialog

import cv2
import os

from img_search import img_search


class Colour:
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    White = "\u001b[37m"
    Red = "\u001b[31m"


os.system('cls' if os.name == 'nt' else 'clear')
print(Colour.Magenta + "\033[1m▒▒▒▒▒ FACE SEEKER ▒▒▒▒▒\033[0m")
print()

face_cascade = cv2.CascadeClassifier()

# face_cascade.load('haarcascade_frontalface_default.xml')
face_cascade.load('haarcascade_frontalface_default2.xml')


# face_cascade.load('haarcascade_profileface.xml')

def detect(image):
    global face_cascade

    img = cv2.imread(image)

    if img is None:
        print("Could not read image.")

    def rectangle_text_contour(place, text, x_axis, y_axis):
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size, _ = cv2.getTextSize(text, font, 1.1, 2)
        text_length, text_height = text_size
        cv2.putText(place, text, (x_axis, y_axis + text_height), font, 1.1, (0, 0, 0), 3)
        cv2.putText(place, text, (x_axis, y_axis + text_height), font, 1.1, (255, 255, 255), 2)

    frame_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame_bw, scaleFactor=1.3,
                                          minNeighbors=8)  # regulate recognition parameters here

    num = 1

    img_h, img_w, _ = img.shape
    fix_width = 650
    rel_height = int(fix_width * (img_h / img_w))
    drawing_coef = fix_width / img_w
    img_resized = cv2.resize(img, (fix_width, rel_height))  # resized image, purely for displaying

    for (x, y, w, h) in faces:
        y1 = round(y * 0.85)  # regulate how to widen space around the face here
        y2 = round((y + h) * 1.15)
        x1 = round(x * 0.85)
        x2 = round((x + w) * 1.15)
        captured_face_img = img[y1:y2, x1:x2]
        captured_filename = f"face{num}.jpg"
        cv2.imwrite(captured_filename, captured_face_img)

        img_search(captured_filename)  # search funcrion

        x1_rs = round(x * drawing_coef)  # coordinates for rectangle on resized image
        x2_rs = round((x + w) * drawing_coef)
        y1_rs = round(y * drawing_coef)
        y2_rs = round((y + h) * drawing_coef)
        cv2.rectangle(img_resized, (x1_rs, y1_rs), (x2_rs, y2_rs), (0, 255, 0), 2)
        rectangle_text_contour(img_resized, str(num), x1_rs, y2_rs)

        os.remove(captured_filename)

        num += 1

    cv2.imshow("Face Seeker", img_resized)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()

    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
    if filepath:
        # filepath = filepath.encode('utf-8').decode('utf-8') # trying to make it recognize paths with cyrillic chars correctly
        # filepath = os.path.normpath(filepath)
        if filepath:
            # print(f"Path: {filepath}") # debug
            detect(str(filepath))
        else:
            print("Path doesn't exist.")


try:
    open_file_dialog()
except Exception as e:
    print(f"\033[1mError:\033[0m {e}")
