#include "robobody.h"

RoboFace::RoboFace(int xRightEyePin, int yRightEyePin, int xLeftEyePin, int yLeftEyePin, int mouthPin, int pinRoll, int pinYaw)
{
    this->rightEye = Eye(xRightEyePin, yRightEyePin);
    this->leftEye = Eye(xLeftEyePin, yLeftEyePin);
    this->mouth = Mouth(mouthPin);
    this->neck = Neck(pinRoll, pinYaw);
}

void ReadSerialInstruction(String line)
{

}
