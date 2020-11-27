#include "robobody.h"

Neck::Neck(int pinRoll, int pinYaw)
{
    this->rollServo.attach(pinRoll);
    this->yawServo.attach(pinYaw);
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

float Neck::GetRoll()
{
    return this->roll;
}

float Neck::GetYaw()
{
    return this->yaw;
}
