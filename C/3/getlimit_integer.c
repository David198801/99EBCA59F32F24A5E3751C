#include <stdio.h>
#include <math.h>
int main(void)
{
    printf("Please enter the bytes of your type.\n");
    short bytes;//bytes_a
    long long limit_positive,limit_negative;
    scanf("%hd",&bytes);
    //bytes_a=bytes*8-1;
    //printf("%hd",bytes_a);
    limit_positive=pow(2.0,bytes*8-1)-1;
    limit_negative=limit_positive*-1-1;
    printf("The limit of your type is (%lld,%lld).\n",limit_negative,limit_positive);
    getchar();
    getchar();
    return 0;
}
