from math import sqrt

import cv2
from cvzone.HandTrackingModule import HandDetector
import socket
import serial

arduino = True
Rpi = False
Unity = False

if arduino:
    ser_arduino = serial.Serial('COM3', baudrate=9600)  # open serial port
if Rpi:
    ser_RPi = serial.Serial('/dev/ttyUSB0')  # open serial port


WIDTH, HEIGHT = 1280, 720

if Unity:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address_port = ('172.20.15.55', 5052)
    client.connect(server_address_port)

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    cam.set(3, WIDTH)
    cam.set(4, HEIGHT)

    detector = HandDetector(maxHands=1, detectionCon=0.5)

    fingers_ang_max = [307, 307, 337, 330, 290]
    fingers_ang_min = [154, 56, 50, 45, 36]

    while True:
        success, img = cam.read()
        hands, img = detector.findHands(img)
        if hands:
            for hand in hands:
                lm_list = hand['lmList']

                thumb_finger = lm_list[1:4 + 1]
                index_finger = lm_list[5:8 + 1]
                middle_finger = lm_list[9:12 + 1]
                ring_finger = lm_list[13:16 + 1]
                pinky_finger = lm_list[17:20 + 1]

                fingers = [thumb_finger, index_finger, middle_finger, ring_finger, pinky_finger]

                fingers_ang = []

                for i in range(5):
                    finger = fingers[i]

                    joint_start = finger[0]
                    joint_end = finger[-1]

                    v = sqrt(sum([(a_i - b_i) ** 2 for a_i, b_i in zip(joint_start, joint_end)]))
                    # if v < fingers_ang_min[i]:
                    #     fingers_ang_min[i] = v
                    #
                    # if v > fingers_ang_max[i]:
                    #     fingers_ang_max[i] = v

                    v_mod = (v - fingers_ang_min[i]) / (fingers_ang_max[i] - fingers_ang_min[i])
                    if v_mod > 1:
                        v_mod = 1

                    if v_mod < 0:
                        v_mod = 0

                    fingers_ang.append(v_mod)

                if fingers_ang[1] > 0.8 and fingers_ang[2] < 0.2 and fingers_ang[3] < 0.2 and fingers_ang[4] > 0.8:
                    print("rock")

                #print(fingers_ang)

                angs_normalized = [int(ang*140) for ang in fingers_ang]

                if arduino:
                    str_send = str.encode(str(angs_normalized).replace(' ', '').replace('[', '').replace(']', ''))
                    print(str_send)
                    ser_arduino.write(str_send)


                data = []
                for lm in lm_list:
                    data.extend([lm[0], HEIGHT - lm[1], lm[2]])

                # for i in data:
                #    i.to_bytes(2, byteorder='big')

                if Unity:
                    client.send(str.encode(str(data)))

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    ser_arduino.close()
