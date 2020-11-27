#include "robobody.h"

Mouth::Mouth(int pin)
{
    this->servo.attach(pin);
    this->boundaries.min = 0;
    this->boundaries.max = 180;
    this->SetPos(90);
}

void Mouth::SetPos(float newPos)
{
    this->pos = fClamp(newPos, this->boundaries);
}

void Mouth::UpdatePos()
{
    this->servo.write(this->pos);
}

void Mouth::SetBoundaries(float min, float max)
{
    this->boundaries.min = min;
    this->boundaries.max = max;
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
