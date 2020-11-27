#include "robobody.h"

RoboFace::RoboFace(int xRightEyePin, int yRightEyePin, int xLeftEyePin, int yLeftEyePin, int mouthPin, int pinRoll, int pinYaw)
{
    this->rightEye = Eye(xRightEyePin, yRightEyePin);
    this->leftEye = Eye(xLeftEyePin, yLeftEyePin);
    this->mouth = Mouth(mouthPin);
    this->neck = Neck(pinRoll, pinYaw);
}

void RoboFace::ReadSerialInstruction(String line)
{

}

void RoboFace::SendBoundaries()
{
    String msg = "\n";
    msg += "RightEye " + this->rightEye.BoundsToString();
    msg += "LeftEye " + this->leftEye.BoundsToString();
    msg += "Mouth " + this->mouth.BoundsToString();
    msg += "Neck " + this->neck.BoundsToString();

    Serial.print(msg);
}