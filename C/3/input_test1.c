#include <stdio.h>
int main(void)
{
    float weight;
    float value;
    printf("please enter weight:");
    scanf("%f",&weight);
    value=weight*1700.0*14.5833;
    printf("the value is %.2f",value);
    return 0;
}
