#include "robobody.h"

Neck::Neck(int pinRoll, int pinYaw)
{
    this->rollServo.attach(pinRoll);
    this->yawServo.attach(pinYaw);
    this->rollBound.min = 0;
    this->yawBound.min = 0;
    this->rollBound.max = 180;
    this->yawBound.max = 180;
}

void Neck::SetPosition(float roll, float yaw)
{
    this->roll = fClamp(roll, this->rollBound);
    this->yaw = fClamp(yaw, this->yawBound);
}

void Neck::Update()
{
    this->rollServo.write(this->roll);
    this->yawServo.write(this->yaw);
}

String Neck::BoundsToString()
{
    String str = "";
    str += "roll: ";
    str += String(this->rollBound.min) + " ";
    str += String(this->rollBound.max) + " ";
    str += "yaw: ";
    str += String(this->yawBound.min) + " ";
    str += String(this->yawBound.max) + "\n";

    return str;
}

float Neck::GetRoll()
{
    return this->roll;
}

float Neck::GetYaw()
{
    return this->yaw;
}
