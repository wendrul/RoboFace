#include "robobody.h"

Mouth::Mouth(int pin)
{
    this->servo.attach(pin);
}

void Mouth::SetPos(float newPos)
{
    this->pos = fClamp(newPos, this->boundaries);
}

void Mouth::UpdatePos()
{
    this->servo.write(this->pos);
}

float Mouth::GetPos()
{
    return this->pos;
}
