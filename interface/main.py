from interface import *
from roboface import *

def main():
    face = RoboFace()
    com = RoboSerialInterface()
    face = com.ReadBounds(face)

main()