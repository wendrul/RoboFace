#include "util.h"
#include <string.h>

float   fClamp(float x, float min, float max)
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

float   fClamp(float x, fboundaries_t boundaries)
{
    return (fClamp(x, boundaries.min, boundaries.max));
}

bool    name_cmp(const char *word, const char *text)
{
    int n = strlen(word);
    return strncmp(word, text, n) == 0;
}

void    next_arg(char **line)
{
    while (**line != ' ') (*line)++;
    while (**line == ' ') (*line)++;
}