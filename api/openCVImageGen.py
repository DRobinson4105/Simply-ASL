import numpy as np
from math import floor
from numpy import array
import cv2
import json
import os
# Full connection array for the entire skeleton based on the keypoints image

width = 960
height = 960

connections = [
    (7, 9), # Legs and abdomen
    (6, 8),
    (8, 10),
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
    (54, 53), # Face
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
    (17, 23), # Feet
    (23, 22),
    (23, 21),
    (16, 20),
    (20, 18),
    (20, 19)
]

#Test function
# def jsonToNumpy(jsn):
#     keypoints = jsn["instance_info"][0]["keypoints"]
#     keypoint_scores = jsn["instance_info"][0]["keypoint_scores"]

#     keypoints, keypoint_scores = np.array(keypoints), np.array(keypoint_scores)

#     return np.concatenate((keypoints, keypoint_scores[:, None]), axis=-1)

def convertWidth(c, min_width, frame_width):
    return (floor(((c - min_width) / frame_width) * width))

def convertHeight(d, min_height, frame_height):
    return floor(((d - min_height) / frame_height) * height)

def generate_scene(keypoint_frame):

    image = np.zeros((height + 150, width + 150, 3), np.uint8)

    #Used for coordinate shift for the image
    min_width, min_height, min_confidence = [min(k) for k in zip(*keypoint_frame)]
    max_width, max_height, max_confidence = [max(k) for k in zip(*keypoint_frame)]

    frame_width = max_width - min_width
    frame_height = max_height - min_height

    for count, (x, y, c) in enumerate(keypoint_frame):

        #Don't plot if low confidence
        if(c < 0.35):
            continue

        #the hands have a keypoint index at 92 and above, so mark them as yellow
        if(count >= 92):
            cv2.circle(image,(convertWidth(x, min_width, frame_width),
                              convertHeight(y, min_height, frame_height)),
                              3, (0,255,255), -1)

        else :
            cv2.circle(image,(convertWidth(x, min_width, frame_width),
                              convertHeight(y, min_height, frame_height)),
                              3, (255,255,255), -1)

    for i in range(len(connections)):
        #If there is a low confidence, don't connect the points (one would not be plotted anyway)
        if(keypoint_frame[connections[i][0] - 1][2] < 0.35 or keypoint_frame[connections[i][1] - 1][2] < 0.35):
            continue

        p1 = [keypoint_frame[connections[i][0] - 1][0], keypoint_frame[connections[i][0] - 1][1]]
        p2 = [keypoint_frame[connections[i][1] - 1][0], keypoint_frame[connections[i][1] - 1][1]]

        if(connections[i][0] >= 92 and connections[i][1]):
            color = (20, 170, 170)

        else :
            color = (250, 230, 230)

        cv2.line(image, (convertWidth(p1[0], min_width, frame_width), convertHeight(p1[1], min_height, frame_height)),
                        (convertWidth(p2[0], min_width, frame_width), convertHeight(p2[1], min_height, frame_height)),
                        color, 3)

    return image

def getVideo(np_keypoint_frame):
    video = cv2.VideoWriter("output2.mp4", cv2.VideoWriter_fourcc(*'MJPG'), 30,(1110, 1110), isColor=True)

    for frame in np_keypoint_frame:
        video_frame = generate_scene(frame)
        video.write(video_frame)
        
    os.rename("output2.mp4", "output.mp4")

    return video