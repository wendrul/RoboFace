from util import mean

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
        self._m = 3
        self._pos_list = []

    def SetBounds(self, minPos, maxPos):
        self.minPos = minPos
        self.maxPos = maxPos

    def SetPosFromRange(self, t):
        pos = (self.maxPos - self.minPos) * (1 - t) + self.minPos
        self._pos_list.append(pos)
        if (len(self._pos_list) > self._m):
            self.pos = mean(self._pos_list)
            self._pos_list.pop(0)


class Neck:
    def __init__(self):
        self.roll = 90
        self.yaw = 90
        self.minRoll = 0
        self.maxRoll = 180
        self.minYaw = 0
        self.maxYaw = 90

    def SetBounds(self, minRoll, maxRoll, minYaw, maxYaw):
        self.minRoll = minRoll
        self.maxRoll = maxRoll
        self.minYaw = minYaw
        self.maxYaw = maxYaw

    def SetPosFromRange(self, troll, tyaw):
        self.roll = (self.maxRoll - self.minRoll) * troll + self.minRoll
        self.yaw = (self.maxYaw - self.minYaw) * tyaw + self.minYaw


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
