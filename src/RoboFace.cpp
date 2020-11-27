#include "robobody.h"

RoboFace::RoboFace(int xRightEyePin, int yRightEyePin, int xLeftEyePin, int yLeftEyePin, int mouthPin, int pinRoll, int pinYaw)
{
    this->rightEye = Eye(xRightEyePin, yRightEyePin);
    this->leftEye = Eye(xLeftEyePin, yLeftEyePin);
    this->mouth = Mouth(mouthPin);
    this->neck = Neck(pinRoll, pinYaw);
}

void RoboFace::ReadSerialInstruction(char *line)
{
    bool valid = true;
    if (name_cmp("ask ", line))
    {
        next_arg(&line);
        if (name_cmp("bound", line))
        {
            this->SendBoundaries();
        }
    }
    else if (name_cmp("RE ", line))
    {
        next_arg(&line);
        float x = atof(line);
        next_arg(&line);
        float y = atof(line);
        this->rightEye.SetPosition(x, y);
    }
    else if (name_cmp("LE ", line))
    {
        next_arg(&line);
        float x = atof(line);
        next_arg(&line);
        float y = atof(line);
        this->leftEye.SetPosition(x, y);
    }
    else if (name_cmp("M ", line))
    {
        next_arg(&line);
        float pos = atof(line);
        this->mouth.SetPos(pos);
    }
    else if (name_cmp("N ", line))
    {
        next_arg(&line);
        float roll = atof(line);
        next_arg(&line);
        float yaw = atof(line);
        this->neck.SetPosition(roll, yaw);
    }
    else
        valid = false;
}

void RoboFace::SendBoundaries()
{
    String msg = "\nBounds:\n";
    msg += "RightEye " + this->rightEye.BoundsToString();
    msg += "LeftEye " + this->leftEye.BoundsToString();
    msg += "Mouth " + this->mouth.BoundsToString();
    msg += "Neck " + this->neck.BoundsToString();

    Serial.print(msg);
}