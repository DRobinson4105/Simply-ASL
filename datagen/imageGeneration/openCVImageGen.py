import numpy as np
from math import floor
import matplotlib.pyplot as plt
import cv2
# Full connection array for the entire skeleton based on the keypoints image

width = 960
height = 960

connections = [
    (4, 8), #Legs and abdomen
    (4, 10),
    (7, 9),
    (9, 11),
    (7, 13),
    (6, 12),
    (12, 14),
    (14, 16),
    (13, 15),
    (15, 17),
    (92, 93),  # Hands (example for the left hand, repeat for right hand)
    (93, 94),
    (94, 95),
    (95, 96),  # Wrist to Thumb
    (97, 98),
    (98, 99),
    (99, 100),  # Other Finger
    (101, 102),
    (102, 103),
    (103, 104),  # Middle Finger
    (105, 106),
    (106, 107),
    (107, 108),  # Other Other Finger
    (109, 110),
    (110, 111),
    (111, 112),  # Pinky
    (92, 109),
    (92, 105),
    (92, 101),
    (92, 97),
    (113, 114),
    (114, 115),
    (115, 116),
    (116, 117),
    (113, 118),
    (118, 119),
    (119, 120),
    (120, 121),
    (113, 122),
    (122, 123),
    (123, 124),
    (124, 125),
    (113, 126),
    (126, 127),
    (127, 128),
    (128, 129),
    (113, 130),
    (130, 131),
    (131, 132),
    (132, 133),
    (54, 53),
    (53, 52),
    (52, 51),
    (51, 46),
    (46, 48),
    (48, 50),
    (50, 40),
    (40, 37),
    (37, 35),
    (35, 32),
    (32, 29),
    (29, 27),
    (27, 25),
    (25, 24),
    (24, 41),
    (41, 43),
    (43, 45),
    (45, 51),
]

def convertWidth(c, min_width, frame_width):
    return (floor(((c - min_width) / frame_width) * width))

def convertHeight(d, min_height, frame_height):
    return floor(((d - min_height) / frame_height) * height)

def generate_scene(keypoint_frame):


    image = np.zeros((height + 150, width + 150, 3), np.uint8)

    min_width, min_height = [min(k) for k in zip(*keypoint_frame)]
    max_width, max_height = [max(k) for k in zip(*keypoint_frame)]

    frame_width = max_width - min_width
    frame_height = max_height - min_height

    for count, (c, d) in enumerate(keypoint_frame):

        if(count >= 92):
            cv2.circle(image,(convertWidth(c, min_width, frame_width),
                              convertHeight(d, min_height, frame_height)),
                              3, (0,255,255), -1)

        else :
            cv2.circle(image,(convertWidth(c, min_width, frame_width),
                              convertHeight(d, min_height, frame_height)),
                              3, (255,255,255), -1)

    for i in range(len(connections)):
        p1 = keypoint_frame[connections[i][0] - 1]
        p2 = keypoint_frame[connections[i][1] - 1]

        cv2.line(image, (convertWidth(p1[0], min_width, frame_width), convertHeight(p1[1], min_height, frame_height)),
                        (convertWidth(p2[0], min_width, frame_width), convertHeight(p2[1], min_height, frame_height)),
                        (20, 170, 170), 3)

    cv2.imwrite("frame.png", image)
