import numpy as np
from math import floor
import matplotlib.pyplot as plt
import cv2
import json
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

def convertWidth(c, min_width, frame_width):
    return (floor(((c - min_width) / frame_width) * width))

def convertHeight(d, min_height, frame_height):
    return floor(((d - min_height) / frame_height) * height)

def generate_scene(keypoint_frame, keypoint_confidence):

    image = np.zeros((height + 150, width + 150, 3), np.uint8)

    #Used for coordinate shift for the image
    min_width, min_height = [min(k) for k in zip(*keypoint_frame)]
    max_width, max_height = [max(k) for k in zip(*keypoint_frame)]

    frame_width = max_width - min_width
    frame_height = max_height - min_height

    for count, (c, d) in enumerate(keypoint_frame):

        #Don't plot if low confidence
        if(keypoint_confidence[count] < 0.3):
            continue

        #the hands have a keypoint index at 92 and above, so mark them as yellow
        if(count >= 92):
            cv2.circle(image,(convertWidth(c, min_width, frame_width),
                              convertHeight(d, min_height, frame_height)),
                              3, (0,255,255), -1)

        else :
            cv2.circle(image,(convertWidth(c, min_width, frame_width),
                              convertHeight(d, min_height, frame_height)),
                              3, (255,255,255), -1)

    for i in range(len(connections)):

        #If there is a low confidence, don't connect the points (one would not be plotted anyway)
        if(keypoint_confidence[connections[i][0] - 1] < 0.3 or keypoint_confidence[connections[i][1] - 1] < 0.3):
            continue

        p1 = keypoint_frame[connections[i][0] - 1]
        p2 = keypoint_frame[connections[i][1] - 1]

        cv2.line(image, (convertWidth(p1[0], min_width, frame_width), convertHeight(p1[1], min_height, frame_height)),
                        (convertWidth(p2[0], min_width, frame_width), convertHeight(p2[1], min_height, frame_height)),
                        (20, 170, 170), 3)

    return image

def go(JSONS):
    video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30,(960, 960), isColor=True)
    for num in range(500):
        for jsn in JSONS:
            video.write(generate_scene(jsn['instance_info'][0]['keypoints'], jsn['instance_info'][0]['keypoint_scores']))

    return video

go([{
    {
        "instance_info": [
            {
                "keypoints": [
                    [
                        314.0784875287221,
                        103.37893773752319
                    ],
                    [
                        333.07814921006684,
                        84.45238553611472
                    ],
                    [
                        292.0009209820074,
                        86.25807268578814
                    ],
                    [
                        358.0123921780023,
                        96.85234077182213
                    ],
                    [
                        261.6481864113771,
                        102.7083353890435
                    ],
                    [
                        386.2634115213948,
                        195.0634238246938
                    ],
                    [
                        217.08981324458273,
                        191.35762715719864
                    ],
                    [
                        419.9377533069651,
                        303.2589675231965
                    ],
                    [
                        163.59524218288016,
                        335.90013166247854
                    ],
                    [
                        425.44815088069333,
                        354.5407429971093
                    ],
                    [
                        182.14991153532844,
                        221.17400879905574
                    ],
                    [
                        355.5292206628941,
                        352.6277956275196
                    ],
                    [
                        242.8501297641078,
                        351.845160741012
                    ],
                    [
                        351.5250548357875,
                        83.96603891340305
                    ],
                    [
                        204.28952886496734,
                        148.36264391329655
                    ],
                    [
                        336.9042941014434,
                        67.88830778660963
                    ],
                    [
                        172.26976460492472,
                        357.52021181086343
                    ],
                    [
                        324.1552586276474,
                        99.94762205238658
                    ],
                    [
                        298.4975299354038,
                        96.18359678297799
                    ],
                    [
                        361.2847308312587,
                        80.63438566491084
                    ],
                    [
                        176.2402945869353,
                        174.92592276649407
                    ],
                    [
                        270.647680305598,
                        82.33460774479215
                    ],
                    [
                        253.47530616260087,
                        187.03604342952076
                    ],
                    [
                        264.12331652908506,
                        91.15308045909978
                    ],
                    [
                        266.19202602072505,
                        99.3660945473896
                    ],
                    [
                        267.74389569811444,
                        106.97270186699052
                    ],
                    [
                        271.3782772656666,
                        114.9661134707303
                    ],
                    [
                        274.72874949664777,
                        122.88581014226065
                    ],
                    [
                        280.2815744432264,
                        130.82783241322193
                    ],
                    [
                        287.55738880366323,
                        137.45902847840875
                    ],
                    [
                        299.8321318569159,
                        142.56674889952637
                    ],
                    [
                        316.9107697108145,
                        143.82191280955084
                    ],
                    [
                        332.94381586618283,
                        140.9557280821507
                    ],
                    [
                        342.3103335402536,
                        134.30612540724047
                    ],
                    [
                        346.5929177497362,
                        126.74127429087883
                    ],
                    [
                        349.7079990754753,
                        118.88969218884688
                    ],
                    [
                        351.26758009290893,
                        111.142456348255
                    ],
                    [
                        352.8304916891168,
                        103.47234875348892
                    ],
                    [
                        353.6327711058615,
                        95.60793512064015
                    ],
                    [
                        352.5028947606995,
                        86.3827850518054
                    ],
                    [
                        274.3847697212882,
                        80.68791780012623
                    ],
                    [
                        280.81290677592585,
                        77.7006805374196
                    ],
                    [
                        287.798060626601,
                        76.23966853252853
                    ],
                    [
                        295.7438914196771,
                        75.50530042893564
                    ],
                    [
                        302.3294658331172,
                        75.43122520251109
                    ],
                    [
                        319.8549413365844,
                        74.53868161755906
                    ],
                    [
                        326.51186814934454,
                        73.89934269342405
                    ],
                    [
                        333.69676671081584,
                        73.81734731521954
                    ],
                    [
                        340.1837739956745,
                        74.20930949548972
                    ],
                    [
                        345.9658387785885,
                        76.1788925873052
                    ],
                    [
                        312.9308180915514,
                        86.55826729738942
                    ],
                    [
                        312.66218140899787,
                        92.64282750787908
                    ],
                    [
                        313.0397670242389,
                        98.31398487182736
                    ],
                    [
                        314.25317788567804,
                        104.18892970057021
                    ],
                    [
                        302.85233669541776,
                        110.24336425792058
                    ],
                    [
                        308.64589347536264,
                        110.67047092653627
                    ],
                    [
                        315.172177585583,
                        110.43194351426928
                    ],
                    [
                        321.20205543240945,
                        109.9872013919695
                    ],
                    [
                        325.9140742672364,
                        109.0341030950841
                    ],
                    [
                        281.4415760234251,
                        88.73372376787609
                    ],
                    [
                        288.1725857099957,
                        85.52319890610397
                    ],
                    [
                        296.5322484170424,
                        85.03054397415332
                    ],
                    [
                        302.3070519381247,
                        88.61157770802214
                    ],
                    [
                        295.55023776735936,
                        90.21415373467312
                    ],
                    [
                        287.44630950076885,
                        90.54939169940155
                    ],
                    [
                        322.596907823995,
                        87.53845719086627
                    ],
                    [
                        326.7180639811893,
                        83.47345983286607
                    ],
                    [
                        334.5256907577525,
                        82.82503138098991
                    ],
                    [
                        341.53685912912147,
                        85.62298144082013
                    ],
                    [
                        336.0930731308729,
                        87.7106525418568
                    ],
                    [
                        329.08475525485085,
                        88.48038004613392
                    ],
                    [
                        296.60585120742576,
                        122.9104618517116
                    ],
                    [
                        303.3903301856651,
                        120.90354722245581
                    ],
                    [
                        311.970411196078,
                        119.2117699332992
                    ],
                    [
                        315.81936005023135,
                        119.10196237007301
                    ],
                    [
                        319.69351328429593,
                        118.56048441150722
                    ],
                    [
                        326.4048095451502,
                        119.35182956868744
                    ],
                    [
                        331.7075110263245,
                        120.77222314154471
                    ],
                    [
                        328.25040026414763,
                        123.72079514612028
                    ],
                    [
                        323.3286449822026,
                        125.88536693874164
                    ],
                    [
                        316.2455541124441,
                        127.23980770739087
                    ],
                    [
                        308.70557384636663,
                        126.98724778359025
                    ],
                    [
                        302.2720058479624,
                        125.37165059758826
                    ],
                    [
                        298.38870102357293,
                        123.00426476664802
                    ],
                    [
                        307.2931083940574,
                        122.2008086670811
                    ],
                    [
                        316.1237329428732,
                        121.52475765871759
                    ],
                    [
                        323.0389746445089,
                        121.17388166086567
                    ],
                    [
                        329.98452161246644,
                        121.11583004558418
                    ],
                    [
                        323.4948438635456,
                        122.94834963285234
                    ],
                    [
                        316.03395734204673,
                        124.01026942458589
                    ],
                    [
                        307.03056276998245,
                        123.99794356986041
                    ],
                    [
                        423.22860517737047,
                        356.62099330150613
                    ],
                    [
                        407.3879224501102,
                        361.0962772771352
                    ],
                    [
                        400.09047433024966,
                        363.4586948404783
                    ],
                    [
                        227.99070755617595,
                        171.70266750912344
                    ],
                    [
                        226.7731259699658,
                        171.06057265029085
                    ],
                    [
                        217.17841864205616,
                        165.8404530759791
                    ],
                    [
                        211.4602649653457,
                        160.5580468491213
                    ],
                    [
                        203.97366397529458,
                        130.06179634441128
                    ],
                    [
                        197.2872420369954,
                        116.4990073319999
                    ],
                    [
                        212.3446086428728,
                        165.95776992916115
                    ],
                    [
                        209.85546609014273,
                        153.25916871488204
                    ],
                    [
                        215.9785401322124,
                        153.1597780791367
                    ],
                    [
                        227.14068984367077,
                        167.91259992101288
                    ],
                    [
                        207.71963493438216,
                        164.6536312896941
                    ],
                    [
                        207.5426041707201,
                        153.47836665855903
                    ],
                    [
                        217.16551639995885,
                        165.0828112302841
                    ],
                    [
                        221.57775313991328,
                        170.6703297687311
                    ],
                    [
                        206.39172417563213,
                        165.1121657273842
                    ],
                    [
                        206.06907810755456,
                        158.33661178003302
                    ],
                    [
                        211.18550721909946,
                        166.669900926639
                    ],
                    [
                        212.7452982730324,
                        170.98411442528607
                    ],
                    [
                        191.81420095492126,
                        217.13264547737276
                    ],
                    [
                        202.78209690977837,
                        202.63483608834008
                    ],
                    [
                        225.61243426984083,
                        187.46585546522493
                    ],
                    [
                        228.17592974330898,
                        176.33851628564298
                    ],
                    [
                        231.7710344854995,
                        171.7775075706361
                    ],
                    [
                        205.72719869718776,
                        157.12981578814157
                    ],
                    [
                        205.91611152566497,
                        140.4173600315463
                    ],
                    [
                        207.4591296648714,
                        129.58232691654132
                    ],
                    [
                        203.27868320445737,
                        118.14409807602709
                    ],
                    [
                        197.28799216735,
                        158.32592937260426
                    ],
                    [
                        207.5492953334823,
                        147.85126632406542
                    ],
                    [
                        225.53796132824618,
                        156.083508745727
                    ],
                    [
                        231.00773184197465,
                        164.969426008712
                    ],
                    [
                        190.21672335197832,
                        164.3416797089701
                    ],
                    [
                        202.61025704816961,
                        153.9384307664253
                    ],
                    [
                        219.55123097941043,
                        161.10656634725854
                    ],
                    [
                        224.19528800411967,
                        169.19265573663165
                    ],
                    [
                        184.38082921482544,
                        169.9539510920863
                    ],
                    [
                        198.22208448998754,
                        160.43274031369674
                    ],
                    [
                        210.37827694201496,
                        163.87092055177277
                    ],
                    [
                        216.54677887835305,
                        168.69440044196978
                    ]
                ],
                "keypoint_scores": [
                    0.9144193530082703,
                    0.9766903519630432,
                    0.9692659974098206,
                    0.9201032519340515,
                    0.9401572942733765,
                    0.8633602261543274,
                    0.6506301760673523,
                    0.44574853777885437,
                    0.609678328037262,
                    0.6554581522941589,
                    0.7803726196289062,
                    0.6560078263282776,
                    0.6894766092300415,
                    0.03889792412519455,
                    0.06732596457004547,
                    0.06907379627227783,
                    0.0364176481962204,
                    0.04203364998102188,
                    0.0524715781211853,
                    0.035463325679302216,
                    0.037686895579099655,
                    0.1144896000623703,
                    0.04095008969306946,
                    0.9857986569404602,
                    0.9870065450668335,
                    0.965193510055542,
                    0.9583401083946228,
                    0.9536473155021667,
                    0.9596182703971863,
                    0.9754590392112732,
                    0.9173880219459534,
                    0.9230217337608337,
                    0.9447569847106934,
                    0.9538378119468689,
                    0.9593778848648071,
                    0.9765150547027588,
                    0.998286247253418,
                    1.0123900175094604,
                    1.008683681488037,
                    0.9450209140777588,
                    0.9955890774726868,
                    0.991470217704773,
                    0.9975375533103943,
                    0.9963481426239014,
                    0.9891413450241089,
                    0.9713076949119568,
                    0.9916084408760071,
                    1.0034326314926147,
                    1.0309524536132812,
                    0.9972506165504456,
                    0.9949190616607666,
                    0.9609648585319519,
                    0.934643566608429,
                    0.9645529389381409,
                    0.9535470008850098,
                    0.9538317322731018,
                    0.9637253284454346,
                    0.9938720464706421,
                    0.9937164187431335,
                    1.0203837156295776,
                    0.9873365163803101,
                    1.000704050064087,
                    1.0166234970092773,
                    0.9968812465667725,
                    0.9908027052879333,
                    0.9968698620796204,
                    1.0133565664291382,
                    1.00217604637146,
                    1.0039745569229126,
                    1.015849232673645,
                    1.0050679445266724,
                    1.0076591968536377,
                    0.9728448390960693,
                    0.9509091973304749,
                    0.9505815505981445,
                    0.9469320774078369,
                    0.9713799953460693,
                    0.9844554662704468,
                    0.9880321025848389,
                    0.9767528772354126,
                    0.9775451421737671,
                    0.9815291166305542,
                    0.9793989658355713,
                    1.0049985647201538,
                    0.9865719676017761,
                    0.9850061535835266,
                    0.979406476020813,
                    0.9919348955154419,
                    0.9963855743408203,
                    0.9845865368843079,
                    0.9869979023933411,
                    0.3360433280467987,
                    0.23508691787719727,
                    0.16032616794109344,
                    0.302566796541214,
                    0.4364207088947296,
                    0.2536609172821045,
                    0.14328375458717346,
                    0.08885431289672852,
                    0.12550023198127747,
                    0.18612666428089142,
                    0.17128954827785492,
                    0.18533562123775482,
                    0.1968698650598526,
                    0.13083086907863617,
                    0.20148807764053345,
                    0.15680453181266785,
                    0.25302085280418396,
                    0.1183287724852562,
                    0.17213840782642365,
                    0.20543374121189117,
                    0.2399681955575943,
                    0.9032262563705444,
                    0.8638110756874084,
                    0.7933498620986938,
                    0.9872061014175415,
                    0.777422308921814,
                    0.7790132164955139,
                    0.9991163611412048,
                    0.9157835841178894,
                    0.879688560962677,
                    0.7924972176551819,
                    0.9893389344215393,
                    0.9346305727958679,
                    1.0167365074157715,
                    0.7795462608337402,
                    0.9348324537277222,
                    1.0168184041976929,
                    0.9834138751029968,
                    0.8914592862129211,
                    0.963372528553009,
                    0.9748759269714355,
                    0.8805585503578186
                ]
            }
        ]
    }
}])