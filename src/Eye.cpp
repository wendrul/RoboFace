#include "robobody.h"

Eye::Eye(int pinX, int pinY)
{
    this->xServo.attach(pinX);
    this->yServo.attach(pinY);
    this->SetPosition(0, 0);
    this->xBoundaries.max = 180;
    this->xBoundaries.min = 0;
    this->xBoundaries.max = 180;
    this->xBoundaries.min = 0;

}

void Eye::SetPosition(float x, float y)
{
    this->x = fClamp(x, this->xBoundaries);
    this->x = fClamp(y, this->yBoundaries);
}

void Eye::SetBoundaries(float xBoundMin, float xBoundMax, float yBoundMin, float yBoundMax)
{
    this->xBoundaries.min = xBoundMin;
    this->xBoundaries.max = xBoundMax;
    this->yBoundaries.min = yBoundMin;
    this->yBoundaries.max = yBoundMax;
}

void Eye::UpdatePos()
{
    this->xServo.write(this->x);
    this->yServo.write(this->y);
}

float Eye::getX()
{
    return x;
}

float Eye::getY()
{
    return y;
}