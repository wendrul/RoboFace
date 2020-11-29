from interface import RoboSerialInterface
from roboface import RoboFace
from gaze_tracking import GazeTracking
import cv2


minH = 0.278
maxH = 0.886
minV = -1.09
maxV = -0.378

def mean(L):
    S = 0
    for x in L:
        S += x
    return S / len(L)


def setup():
    face = RoboFace()
    com = RoboSerialInterface(baudrate=115200)
    #print("Opening Connection")
    print(f"Connection established on port {com.ser.port}")
    face = com.ReadBounds(face)
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    return face, gaze, webcam, com


hs, vs = [], []
mov_mean = 1


def loop(face: RoboFace, gaze: GazeTracking, webcam: cv2.VideoCapture, com: RoboSerialInterface):
    _, frame = webcam.read()
    gaze.refresh(frame)
    h, v = gaze.horizontal_ratio(), gaze.vertical_ratio()
    if (not(h == None or v == None)):
        hs.append(h)
        vs.append(-v)
    else:
        if (len(hs) > 0):
            hs.pop(0)
            vs.pop(0)
    if (len(hs) > mov_mean):
        tempH = (mean(hs) - minH) / (maxH - minH)
        tempV = (mean(vs) - minV) / (maxV - minV)
        face.rightEye.SetPosFromRange(tempH, 1 - tempV)
        face.leftEye.SetPosFromRange(tempH, tempV)
        hs.pop(0)
        vs.pop(0)
        com.SendStatus(face)
    frame = gaze.annotated_frame()
    cv2.imshow("Rtuber-chan", frame)
    if cv2.waitKey(1) == 27:
        return True
    else:
        return False


def main():
    print("does this even print")
    face, gaze, webcam, com = setup()
    while (True):
        end = loop(face, gaze, webcam, com)
        if (end):
            break

try:
    main()
except KeyboardInterrupt:
    print("^C") #huashuahsuahsuahsauhsahusa
    exit()
