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

    def SetPosFromRange(self, tx, ty):
        self.x = (self.xMax - self.xMin) * tx + self.xMin
        self.y = (self.yMax - self.yMin) * ty + self.yMin


class Mouth:
    def __init__(self):
        self.pos = 90
        self.minPos = 0
        self.maxPos = 180

    def SetBounds(self, minPos, maxPos):
        self.minPos = minPos
        self.maxPos = maxPos

    def SetPosFromRange(self, t):
        self.x = (self.maxPos - self.minPos) * t + self.minPos


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

    def SetPosFromRange(self, troll, tyaw):
        self.x = (self.minRoll - self.maxRoll) * troll + self.minRoll
        self.y = (self.minYaw - self.maxYaw) * tyaw + self.minYaw


class RoboFace:
    def __init__(self):
        self.rightEye = Eye()
        self.leftEye = Eye()
        self.mouth = Mouth()
        self.neck = Neck()

    def Serialize(self):
        msg = ""
        msg += f"RE {self.rightEye.x} {self.rightEye.y}\n"
        msg += f"LE {self.leftEye.x} {self.leftEye.y}\n"
        msg += f"M {self.mouth.pos}\n"
        msg += f"N {self.neck.roll} {self.neck.yaw}\n"
        return msg
