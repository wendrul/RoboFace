#include <Arduino.h>
#include <Servo.h>
#include "robobody.h"
#include "bounds_pins.h"


/*RoboFace     face = RoboFace(X_RIGHT_EYE_PIN, Y_RIGHT_EYE_PIN, 
                    X_LEFT_EYE_PIN, Y_LEFT_EYE_PIN,
                    MOUTH_PIN,
                    ROLL_NECK_PIN, YAW_NECK_PIN);*/
RoboFace face;
char buf[1024];
int cur = 0;

void setup()
{
    Serial.begin(9600);

    face = RoboFace(X_RIGHT_EYE_PIN, Y_RIGHT_EYE_PIN, 
                    X_LEFT_EYE_PIN, Y_LEFT_EYE_PIN,
                    MOUTH_PIN,
                    ROLL_NECK_PIN, YAW_NECK_PIN);
    face.rightEye.SetBoundaries(RIGHT_EYE_X_BOUND_MIN, RIGHT_EYE_X_BOUND_MAX,
                                RIGHT_EYE_Y_BOUND_MIN, RIGHT_EYE_Y_BOUND_MAX);
    face.leftEye.SetBoundaries(LEFT_EYE_X_BOUND_MIN, LEFT_EYE_Y_BOUND_MAX,
                                LEFT_EYE_Y_BOUND_MIN, LEFT_EYE_Y_BOUND_MAX);
    face.mouth.SetBoundaries(MOUTH_BOUND_MIN, MOUTH_BOUND_MAX);
    face.neck.SetBoundaries(ROLL_BOUND_MIN, ROLL_BOUND_MAX,
                            YAW_BOUND_MIN, YAW_BOUND_MAX);   
}

void UpdatePos()
{
    face.rightEye.UpdatePos();
    face.leftEye.UpdatePos();
    face.mouth.UpdatePos();
    face.neck.UpdatePos();
}

void ClearBuf()
{
    cur = 0;
    buf[0] = '\0';
}

void loop()
{
    UpdatePos();
    if(Serial.available())
    {
        int i = cur;
        cur += Serial.readBytesUntil('\n', buf + cur, 1023 - cur);
        buf[cur] = '\0';
        Serial.println(buf + i);
        if (buf[cur - 1] == '\r')
        {
            Serial.println(buf);
            face.ReadSerialInstruction(buf);
            ClearBuf();
            UpdatePos();
        }
    }
}