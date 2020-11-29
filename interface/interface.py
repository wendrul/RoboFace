import serial, time
from roboface import RoboFace


class RoboSerialInterface:
    def __init__(self, baudrate=9600, port='COM4', timeout = 1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout, write_timeout=timeout)
        time.sleep(3)
    def ReadBounds(self, face: RoboFace) -> RoboFace:
        self.ser.write(b'ask bound\n')
        boundsLines = []
        while (len(boundsLines) < 6):
            line = self.ser.readline().decode()
            if (line):
                boundsLines.append(line)
        if (len(boundsLines) < 4):
            raise Exception("Failed to read Boundaries from Serial")
        for lineRaw in boundsLines:
            line = str(lineRaw).split(' ')
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

    def SendStatus(self, face: RoboFace):
        self.ser.write(face.Serialize().encode())

    def CloseConnection(self):
        self.ser.close()
