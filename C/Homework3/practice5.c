#include <stdio.h>
int main(void)
{
    float seconds=3.156e7;
    //double seconds;
    short years;
    printf("enter your age(year)\n");
    scanf("%hd",&years);
    seconds=seconds*years;
    printf("your age is %e seconds\n",seconds);
    getchar();
    getchar();
    return 0;
}
