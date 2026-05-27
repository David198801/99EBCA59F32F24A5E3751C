#include <stdio.h>
int main(void)
{
    float pints,cups,oz,spoons,teaspoons;
    printf("enter the amount of cups\n");
    scanf("%f",&cups);
    pints=cups/2;
    oz=cups*8;
    spoons=oz*2;
    teaspoons=spoons*3;
    printf("%f cup(s)=%f pints\n",cups,pints);
    printf("%f cup(s)=%f oz\n",cups,oz);
    printf("%f cup(s)=%f spoons\n",cups,spoons);
    printf("%f cup(s)=%f teaspoons\n",cups,teaspoons);
    getchar();
    getchar();
    return 0;
}
