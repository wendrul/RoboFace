#include "robobody.h"

Eye::Eye(int pinX, int pinY)
{
    this->xServo.attach(pinX);
    this->yServo.attach(pinY);
    this->SetPosition(90., 90.);
    this->xBoundaries.max = 180.;
    this->xBoundaries.min = 0.;
    this->xBoundaries.max = 180.;
    this->xBoundaries.min = 0.;

}

void Eye::SetPosition(float x, float y)
{
    this->x = fClamp(x, this->xBoundaries);
    this->y = fClamp(y, this->yBoundaries);
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

String Eye::BoundsToString()
{
    String str = "";
    str += "x: ";
    str += String(this->xBoundaries.min) + " ";
    str += String(this->xBoundaries.max) + " ";
    str += "y: ";
    str += String(this->yBoundaries.min) + " ";
    str += String(this->yBoundaries.max) + "\n";

    return str;
}

float Eye::GetX()
{
    return x;
}

float Eye::GetY()
{
    return y;
}
