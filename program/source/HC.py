import numpy
import math
import cv2
import autopy
import mediapipe
import pyautogui

import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor


print("Loaded")


def read(file_path):
    print("reading from "+file_path)
    with open(file_path, 'r') as file:
        text = file.read()
        number = int(text)
        return number


px, py = 0, 0
cx, cy = 0, 0
cameraWidth, cameraHeight = read("./cw"), read(
    "./ch")
c = cv2.VideoCapture(read("./camnum"))
c.set(3, cameraWidth)
c.set(4, cameraHeight)
screenWidth, screenHeight = autopy.screen.size()

minlength = read("./ml")
print("init-success")


try:
    all = None
    results = None
    mode = False
    maxHands = 2
    detectionCon = 0.8
    trackCon = 0.8
    model_complexity = 1
    mpHands = mediapipe.solutions.hands
    hands = mpHands.Hands(mode, maxHands, model_complexity, detectionCon, trackCon)
    results = None
except Exception as e:
    print(e)
    exit(0)


def search(img):
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return img, results

def pos(image, results):
    all = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                all.append([id, cx, cy])
    return all

def finddis(all, p0, p1, image):
    x1, y1 = all[p0][1:]
    x2, y2 = all[p1][1:]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    return math.hypot(x2 - x1, y2 - y1), image, [x1, y1, x2, y2, cx, cy]



class CircleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(20, 20)

    def setWindowPosition(self, x, y):
        self.move(x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.white)
        painter.setBrush(QColor(128, 128, 128, 180))
        painter.drawEllipse(0, 0, 20, 20)




print("model created")
pressed = False



if __name__ == '__main__':
    app = QApplication(sys.argv)
    circle_window1 = CircleWindow()
    circle_window1.setWindowPosition(100, 100)
    circle_window1.show()
    circle_window2 = CircleWindow()
    circle_window2.setWindowPosition(100, 100)
    circle_window2.show()

    while True:
        print("running")
        try:
            success, handimg = c.read()
            img, results = search(handimg)
            ah = pos(img, results)
            if len(ah) != 0:
                x1, y1 = ah[4][1:]
                x2, y2 = ah[8][1:]
                x3, y3 = ah[20][1:]
                fx = numpy.interp((x1*0.8 + x2*0.2), (100, cameraWidth - 100), (0, screenWidth))
                fy = numpy.interp((y1*0.8 + y2*0.2), (100, cameraHeight - 100), (0, screenHeight))
                
                fx1 = numpy.interp((x1), (100, cameraWidth - 100), (0, screenWidth))
                fy1 = numpy.interp((y1), (100, cameraHeight - 100), (0, screenHeight))
                cx1 = px + (fx1 - px) / 5
                cy1 = py + (fy1 - py) / 5

                fx2 = numpy.interp((x2), (100, cameraWidth - 100), (0, screenWidth))
                fy2 = numpy.interp((y2), (100, cameraHeight - 100), (0, screenHeight))
                cx2 = px + (fx2 - px) / 5
                cy2 = py + (fy2 - py) / 5

                cx = px + (fx - px) / 5
                cy = py + (fy - py) / 5
                autopy.mouse.move(screenWidth - cx, cy)
                circle_window1.setWindowPosition(screenWidth - cx1, cy1)
                circle_window2.setWindowPosition(screenWidth - cx2, cy2)
                QApplication.processEvents()
                px, py = cx, cy
                length1, img, pointInfo = finddis(ah, 4, 8, img)
                length2 = math.hypot(x3 - x1, y3 - y1)
                if length1 < minlength:
                    autopy.mouse.toggle(down=True)
                else:
                    autopy.mouse.toggle(down=False)
            
                if length2 < minlength:
                    if pressed == False:
                        pressed = True
                        pyautogui.hotkey('win', 'h')
                else:
                    if pressed == True:
                        pressed = False
                        pyautogui.press('esc')

        except Exception as e:
            print(e)
            exit(0)