#include "robobody.h"

Mouth::Mouth(int pin)
{
    this->servo.attach(pin);
    this->boundaries.min = 0;
    this->boundaries.max = 180;
}

void Mouth::SetPos(float newPos)
{
    this->pos = fClamp(newPos, this->boundaries);
}

void Mouth::UpdatePos()
{
    this->servo.write(this->pos);
}

String Mouth::BoundsToString()
{
    String str = "";
    str += String(this->boundaries.min) + " ";
    str += String(this->boundaries.max) + "\n";

    return str;
}

float Mouth::GetPos()
{
    return this->pos;
}
