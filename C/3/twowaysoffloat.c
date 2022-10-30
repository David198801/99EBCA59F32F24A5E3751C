#include <stdio.h>
int main(void)
{
    float aboat = 32000.0;
    double abet = 2.14e9;
    long double dip=5.32e-5;
    printf("%f can be weittern %e\n",aboat,aboat);
    printf("%f can be wrinttern %e\n",abet,abet);
    printf("%Lf can be wrinttern %Le\n",dip,dip);
    return 0;
}
