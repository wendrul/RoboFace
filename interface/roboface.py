class Eye:
    def __init__(self):
        self.x = 90
        self.y = 90
        self.xMin = 0
        self.xMax = 180
        self.yMin = 0
        self.yMax = 180
    def SetBounds(self, xMin, xMax, yMin, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax

class Mouth:
    def __init__(self):
        self.pos = 90
        self.minPos = 0
        self.maxPos = 180
    def SetBounds(self, minPos, maxPos):
        self.minPos = minPos
        self.maxPos = maxPos

class Neck:
    def __init__(self):
        self.roll = 90
        self.yaw = 90
        self.minRoll = 0
        self.maxRoll = 180
        self.minYaw = 0
        self.maxRoll = 90
    def SetBounds(self, minRoll, maxRoll, minYaw, maxYaw):
        self.minRoll = minRoll
        self.maxRoll = maxRoll
        self.minYaw = minYaw
        self.maxYaw = maxYaw

class RoboFace:
    def __init__(self):
        self.rightEye = Eye()
        self.leftEye = Eye()
        self.mouth = Mouth()
        self.neck = Neck()