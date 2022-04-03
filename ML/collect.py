import cv2
from cvzone.HandTrackingModule import HandDetector
from math import sqrt
import csv

WIDTH, HEIGHT = 1280, 720

FLATTEN_LIST = True  # True - jedna długa lista [x1, y1, z1, x2, y2, z2, ...],
                     # False - lista list [[x1, y1, z1], [x2, y2, z2], ...]


PARAM_NAME = 'SYF' # jaki gest trenujemy

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    cam.set(3, WIDTH)
    cam.set(4, HEIGHT)

    detector = HandDetector(maxHands=1, detectionCon=0.5)
    n = 0

    with open(f'{PARAM_NAME}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        while n < 3000:
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

                    # print(lm_list)
                    # f.write(str(lm_list) + '\n')
                    normalization_point0 = lm_list[0]
                    normalization_point1 = lm_list[5]

                    normalization = sqrt(sum([(a_i - b_i) ** 2 for a_i, b_i in zip(normalization_point0, normalization_point1)]))

                    fingers_ang = []

                    for i in range(4):
                        finger = fingers[i]

                        joint_start = finger[0]
                        joint_end = finger[-1]

                        v = sqrt(sum([(a_i - b_i) ** 2 for a_i, b_i in zip(joint_start, joint_end)]))
                        v = v/normalization
                        print(v)
                        # if v < fingers_ang_min[i]:
                        #     fingers_ang_min[i] = v
                        #
                        # if v > fingers_ang_max[i]:
                        #     fingers_ang_max[i] = v
                        #
                        # print(fingers_ang_max, "\n", fingers_ang_min)

                        # v_mod = (v - fingers_ang_min[i]) / (fingers_ang_max[i] - fingers_ang_min[i])
                        # if v_mod > 1:
                        #     v_mod = 1

                        # if v_mod < 0:
                        #     v_mod = 0

                        # print(v, v_mod)

                        fingers_ang.append(v)
                    fingers_ang.append(4)
                    writer.writerow(fingers_ang)
                    n+=1


            cv2.imshow("Image", img)
            cv2.waitKey(50)
