import serial
from roboface import *

class RoboSerialInterface:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = 'COM4'
    def ReadBounds(self, face : RoboFace) -> RoboFace:
        self.ser.write("ask bounds")
        boundsLines = self.ser.readlines()
        if (len(boundsLines) < 4):
            raise Exception("Failed to read Boundaries from Serial")
        while line in boundsLines:
            line = str(line).split(' ')
            if (line[0] == "RightEye"):
                face.rightEye.xMin = float(line[2])
                face.rightEye.xMax = float(line[3])
                face.rightEye.yMin = float(line[5])
                face.rightEye.yMax = float(line[6])
            elif (line[0] == "LeftEye"):
                face.leftEye.xMin = float(line[2])
                face.leftEye.xMax = float(line[3])
                face.leftEye.yMin = float(line[5])
                face.leftEye.yMax = float(line[6])
            elif (line[0] == "Mouth"):
                face.mouth.minPos = float(line[1])
                face.mouth.maxPos = float(line[2])
            elif (line[0] == "Neck"):
                face.neck.minRoll = float(line[2])
                face.neck.maxRoll = float(line[3])
                face.neck.minYaw = float(line[5])
                face.neck.maxYaw = float(line[6])
        return face
    def SendStatus(self, face : RoboFace):
        msg = ""
        msg += f"RE {face.rightEye.x} {face.rightEye.y}\n"
        msg += f"LE {face.leftEye.x} {face.leftEye.y}\n"
        msg += f"M {face.mouth.pos}\n"
        msg += f"N {face.neck.roll} {face.neck.yaw}\n"
        self.ser.write(msg)
    def OpenConnection(self):
        self.ser.open()
    def CloseConnection(self):
        self.ser.close()
    def OpenConnection(self, baudrate):
        self.ser.baudrate = baudrate
        self.ser.open()
    def OpenConnection(self, baudrate, port):
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.open()