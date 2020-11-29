from gaze_tracking import GazeTracking
import cv2, time

def mean(L):
    S = 0
    for x in L:
        S += x
    return S / len(L)

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
stockh = []
stockv = []
t = time.time()
hs = []
vs = []
mov_mean = 1
vert0 = []
vert1 = []
hori0 = []
hori1 = []
c = 0
while (True):
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
    text = "No gaze"
    if (len(hs) > mov_mean):
        stockh.append(mean(hs))
        stockv.append(mean(vs))        
        hs.pop(0)
        vs.pop(0)
        text = f"v: {mean(vs)}, h: {mean(hs)}"
    frame = gaze.annotated_frame()
    cv2.putText(frame, text, (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.imshow("pupi", frame)
    if (time.time() > t + 2):
        vert0.append(min(stockv))
        vert1.append(max(stockv))
        hori0.append(min(stockh))
        hori1.append(max(stockh))
        c += 1
        t = time.time()
    if cv2.waitKey(1) == 27 or c > 15:
        break

print(f"horiz: [{mean(hori0)} - {mean(hori1)}]")
print(f"verti: [{mean(vert0)} - {mean(vert1)}]")