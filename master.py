import cv2
from cvzone.HandTrackingModule import HandDetector

WIDTH, HEIGHT = 1280, 720


if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    cam.set(3, WIDTH)
    cam.set(4, HEIGHT)

    detector = HandDetector(maxHands=1, detectionCon=0.5)

    while True:
        success, img = cam.read()
        hands, img = detector.findHands(img)
        if hands:
            for hand in hands:
                ln_list = hand['lnList']

        cv2.imshow("Image", img)
        cv2.waitKey(1)
