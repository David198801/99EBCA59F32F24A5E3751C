#include <stdio.h>
int main(void)
{
    float centers_of_1feet=2.54,centers,feets;
    printf("enter your high(feet)\n");
    scanf("%f",&feets);
    centers=feets*centers_of_1feet;
    printf("your high is %f centers",centers);
    getchar();
    getchar();
    return 0;
}
