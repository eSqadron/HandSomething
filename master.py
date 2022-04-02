import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

WIDTH, HEIGHT = 1280, 720

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address_port = ('127.0.0.1', 5052)


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
                lm_list = hand['lmList']
                data = []
                for lm in lm_list:
                    data.extend([lm[0], HEIGHT - lm[1], lm[2]])

                sock.sendto(str.encode(str(data)), server_address_port)


        cv2.imshow("Image", img)
        cv2.waitKey(1)
