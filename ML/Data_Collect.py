import cv2
from cvzone.HandTrackingModule import HandDetector

WIDTH, HEIGHT = 1280, 720

FLATTEN_LIST = True  # True - jedna długa lista [x1, y1, z1, x2, y2, z2, ...],
                     # False - lista list [[x1, y1, z1], [x2, y2, z2], ...]


PARAM_NAME = 'Rock' # jaki gest trenujemy

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    cam.set(3, WIDTH)
    cam.set(4, HEIGHT)

    detector = HandDetector(maxHands=1, detectionCon=0.5)

    F = open(f'{PARAM_NAME}.txt', 'w')

    while True:
        success, img = cam.read()
        hands, img = detector.findHands(img)

        if hands:
            for hand in hands:
                lm_list = hand['lmList']

                if FLATTEN_LIST:
                    lm_list = [j for i in lm_list for j in i]

                print(lm_list)
                F.write(str(lm_list) + '\n')

        cv2.imshow("Image", img)
        cv2.waitKey(500)
