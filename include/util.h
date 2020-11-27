#ifndef UTIL_H
# define UTIL_H

typedef struct fboundaries_s
{
    float min;
    float max;
} fboundaries_t;


float   fClamp(float x, float min, float max);
float   fClamp(float x, fboundaries_t boundaries);

#endif