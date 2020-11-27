#include <Arduino.h>
#include <Servo.h>
#include "robobody.h"

#define A 30
#define OMEGA 5
#define INITIAL_ANGLE 72
#define SET_ZERO 0

#define X_RIGHT_EYE_PIN 0
#define Y_RIGHT_EYE_PIN 0
#define X_LEFT_EYE_PIN 0
#define Y_LEFT_EYE_PIN 0
#define MOUTH_PIN 0
#define ROLL_NECK_PIN 0
#define YAW_NECK_PIN 0

Servo eye1x;
Servo eye2x;
int    chooseAxis;
bool    pressed;

void setup()
{
    RoboFace face = RoboFace(0, 0, 0, 0, 0, 0, 0);
    pressed = true;
    chooseAxis = 0;
    pinMode(A0, INPUT);
    pinMode(4, INPUT);
    eye1x.attach(3);
    eye2x.attach(5);
    if (SET_ZERO)
    {
        eye2x.write(INITIAL_ANGLE);
        eye1x.write(INITIAL_ANGLE);
        while(1){}
    }
    Serial.begin(9600);
}

void loop()
{
    if (digitalRead(4) == HIGH)
    {
        if (!pressed)
        {
            chooseAxis = (chooseAxis + 1) % 2;
            Serial.println("Pressed");
        }
        pressed = true;
    }
    else
    {
        if (pressed)
            Serial.println("Release");
        pressed = false;
    }
    float t = (float)analogRead(A0) / 1024.;    
    if (!pressed && chooseAxis == 0)
    {
        eye1x.write(180 * t);
    }
    else if (chooseAxis == 1)
    {
        eye2x.write(180 * t);
    }
    //Serial.println(180 * t);
}