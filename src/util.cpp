#include "util.h"

float fClamp(float x, float min, float max)
{
    if (x < min)
    {
        return min;
    }
    if (x > max)
    {
        return max;
    }
    return x;    
}

float fClamp(float x, fboundaries_t boundaries)
{
    return (fClamp(x, boundaries.min, boundaries.max));
}