from util import mean

class Eye:
    def __init__(self):
        self.x = 90
        self.y = 90
        self.xMin = 0
        self.xMax = 180
        self.yMin = 0
        self.yMax = 180
        self._m = 3
        self._x_list = []
        self._y_list = []

    def SetBounds(self, xMin, xMax, yMin, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax

    def SetPosFromRange(self, tx, ty):
        x = (self.xMax - self.xMin) * tx + self.xMin
        y = (self.yMax - self.yMin) * ty + self.yMin
        self._x_list.append(x)
        self._y_list.append(y)
        if (len(self._x_list) > self._m):
            self.x = mean(self._x_list)
            self.y = mean(self._y_list)
            self._x_list.pop(0)
            self._y_list.pop(0)


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
        self._m = 6
        self._roll_list = []
        self._yaw_list = []

    def SetBounds(self, minRoll, maxRoll, minYaw, maxYaw):
        self.minRoll = minRoll
        self.maxRoll = maxRoll
        self.minYaw = minYaw
        self.maxYaw = maxYaw

    def SetPosFromRange(self, troll, tyaw):
        roll = (self.maxRoll - self.minRoll) * (1 - troll) + self.minRoll
        yaw = (self.maxYaw - self.minYaw) * tyaw + self.minYaw
        self._roll_list.append(roll)
        self._yaw_list.append(yaw)
        if (len(self._roll_list) > self._m):
            self.roll = mean(self._roll_list)
            self.yaw = mean(self._yaw_list)
            self._roll_list.pop(0)
            self._yaw_list.pop(0)


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
