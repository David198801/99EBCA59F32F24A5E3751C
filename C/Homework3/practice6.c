#include <stdio.h>
int main(void)
{
    float m_water=3.0e-23;
    short m_quart=950,quarts;
    double molecules_water;
    printf("enter the amount of quart\n");
    scanf("%hd",&quarts);
    molecules_water=quarts*m_quart/m_water;
    printf("there are %e molecules in %d quarts of water.",molecules_water,quarts);
    getchar();
    return 0;
}
