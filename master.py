from math import sqrt

#import time
import cv2
from cvzone.HandTrackingModule import HandDetector
import socket
import serial

arduino = False  # Ręka + ekran
arduino2 = False  # diody + drzwi
arduino3 = False  # wózek
Unity = False

if arduino:
    ser_arduino = serial.Serial('COM4', baudrate=9600)  # open serial port
if arduino2:
    ser_arduino2 = serial.Serial('COM3', baudrate=9600)  # open serial port

WIDTH, HEIGHT = 1280, 720

if Unity:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address_port = ('172.20.15.244', 5052)
    client.connect(server_address_port)

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    cam.set(3, WIDTH)
    cam.set(4, HEIGHT)

    detector = HandDetector(maxHands=1, detectionCon=0.5)

    #fingers_ang_max = [307, 307, 337, 330, 290]
    #fingers_ang_min = [154, 56, 50, 45, 36] #kamyra w lapku

    fingers_ang_max = [184.92160501142098, 162.93863875704866, 174.94284781036347, 167.2154299100415, 142.2708684165525] # zakresy stacjonarki
    fingers_ang_min = [30.23243291566195, 35.58089374931439, 19.4164878389476, 17.916472867168917, 17.74823934929885]


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
                    #
                    # print(fingers_ang_max, "\n", fingers_ang_min)

                    v_mod = (v - fingers_ang_min[i]) / (fingers_ang_max[i] - fingers_ang_min[i])
                    if v_mod > 1:
                        v_mod = 1

                    if v_mod < 0:
                        v_mod = 0

                    print(v, v_mod)

                    fingers_ang.append(v_mod)

                #print(fingers_ang)

                if fingers_ang[1] > 0.8 and fingers_ang[2] < 0.2 and fingers_ang[3] < 0.2 and fingers_ang[4] > 0.8:
                    print("rock")

                if arduino2:
                    print(fingers_ang)
                    if fingers_ang[0] < 0.6:
                        str_send = None
                        if fingers_ang[1] < 0.4 and fingers_ang[2] < 0.4 and fingers_ang[3] < 0.4:
                            str_send = f"G {int(fingers_ang[4] * 100)}"
                        elif fingers_ang[1] < 0.7 and fingers_ang[2] < 0.5 and (
                                fingers_ang[3] > 0.4 and fingers_ang[3] < 0.6):
                            str_send = f"R {int(fingers_ang[4] * 100)}"
                        elif fingers_ang[1] > 0.5 and fingers_ang[2] < 0.7 and fingers_ang[3] < 0.6:
                            str_send = f"B {int(fingers_ang[4] * 100)}"
                        #time.sleep(1)
                        print(str_send)

                        if str_send is not None:
                            str_send_bin = str.encode(str_send)
                            print(str_send_bin)
                            ser_arduino2.write(str_send_bin)
                            for i in range(len(str_send) + 2):
                                print(ser_arduino2.read())

                if arduino:
                    angs_normalized = [int(ang * 140) for ang in fingers_ang]

                    str_send = str(angs_normalized).replace(' ', '').replace('[', '').replace(']', '')
                    str_send_bin = str.encode(str_send)
                    print(str_send_bin)
                    ser_arduino.write(str_send_bin)
                    for i in range(len(str_send) + 2 * 5 - 4):
                        print(ser_arduino.read())

                data = []
                for lm in lm_list:
                    data.extend([lm[0], HEIGHT - lm[1], lm[2]])

                if Unity:
                    client.send(str.encode(str(data)))

        cv2.imshow("Image", img)
        cv2.waitKey(50)
