#include<stdio.h>
int main(void)
{
    float a;
    printf("Enter a floating-point value:");
    scanf("%f",&a);
    printf("fixd-point notation:%f\n",a);
    printf("exponetial notation:%e\n",a);
    printf("p notation:%a\n",a);
    getchar();
    getchar();
    return 0;
}
