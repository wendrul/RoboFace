#include <Arduino.h>
#include <Servo.h>
#include "robobody.h"
#include "bounds_pins.h"

RoboFace *face;
char buf[1024];
int cur = 0;

void UpdatePos()
{
    face->rightEye->UpdatePos();
    face->leftEye->UpdatePos();
    face->mouth->UpdatePos();
    face->neck->UpdatePos();
}

void setup()
{
    Serial.begin(115200);
    pinMode(7, OUTPUT);
    face = new RoboFace(X_RIGHT_EYE_PIN, Y_RIGHT_EYE_PIN,
                        X_LEFT_EYE_PIN, Y_LEFT_EYE_PIN,
                        MOUTH_PIN,
                        ROLL_NECK_PIN, YAW_NECK_PIN);
    face->rightEye->SetBoundaries(RIGHT_EYE_X_BOUND_MIN, RIGHT_EYE_X_BOUND_MAX,
                                 RIGHT_EYE_Y_BOUND_MIN, RIGHT_EYE_Y_BOUND_MAX);
    face->leftEye->SetBoundaries(LEFT_EYE_X_BOUND_MIN, LEFT_EYE_Y_BOUND_MAX,
                                LEFT_EYE_Y_BOUND_MIN, LEFT_EYE_Y_BOUND_MAX);
    face->mouth->SetBoundaries(MOUTH_BOUND_MIN, MOUTH_BOUND_MAX);
    face->neck->SetBoundaries(ROLL_BOUND_MIN, ROLL_BOUND_MAX,
                             YAW_BOUND_MIN, YAW_BOUND_MAX);
}

void ClearBuf()
{
    cur = 0;
    buf[0] = '\0';
}

//Bro did you really just pause the video to look at the code? get a life and also it's on github
void loop()
{
    if (Serial.available())
    {
        digitalWrite(7, HIGH);
        buf[cur] = Serial.read();
        if (buf[cur] != -1)
            cur++;
        buf[cur] = '\0';
        //Serial.print(buf[cur - 1]); //debug
        if (buf[cur - 1] == '\n' || buf[cur - 1] == '\r')
        {
            digitalWrite(7, LOW);
            face->ReadSerialInstruction(buf);
            ClearBuf();
            UpdatePos();
        }
    }
}