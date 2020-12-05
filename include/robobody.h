#ifndef ROBOBODY_H
# define ROBOBODY_H

#include <Servo.h>
#include <Arduino.h>
#include "util.h"   

class Eye
{
private:
    float x;
    float y;
    fboundaries_t xBoundaries;
    fboundaries_t yBoundaries;
    Servo xServo;
    Servo yServo;
public:
    Eye(int pinX, int pinY);
    Eye() = default;
    void SetPosition(float x, float y);
    void SetBoundaries(float xBoundMin, float xBoundMax, float yBoundMin, float yBoundMax);
    void UpdatePos();
    float GetX();
    float GetY();
    String BoundsToString();
};

class Mouth
{
private:
    float pos;
    fboundaries_t boundaries;
    Servo servo;
public:
    Mouth(int pin);
    Mouth() = default;
    void SetPos(float newPos);
    void SetBoundaries(float min, float max);
    void UpdatePos();
    float GetPos();
    String BoundsToString();
};

class Neck
{
private:
    float roll;
    float yaw;
    fboundaries_t yawBound;
    fboundaries_t rollBound;
    Servo rollServo;
    Servo yawServo;
public:
    Neck(int pinRoll, int pinYaw);
    Neck() = default;
    void SetPosition(float roll, float yaw);
    void SetBoundaries(float rollMin, float rollMax, float yawMin, float yawMax);
    void UpdatePos();
    float GetRoll();
    float GetYaw();
    String BoundsToString();
};

class RoboFace
{
private:
public:
    Eye *rightEye;
    Eye *leftEye;
    Mouth *mouth;
    Neck *neck; 
    RoboFace() = default;
    RoboFace(int xRightEyePin, int yRightEyePin, int xLeftEyePin, int yLeftEyePin, int mouthPin, int pinRoll, int pinYaw);
    void ReadSerialInstruction(char *line);
    void SendBoundaries();
};

#endif