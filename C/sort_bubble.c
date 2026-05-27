#include <stdio.h>
int main()
{
    int i,j,t;
    int a[10];
    printf("输入10个数字：\n");
    for (i=0;i<10;i++)
        scanf("%d",&a[i]);
    for (i=0;i<9;i++)
        for (j=0;j<9-i;j++)
            if (a[j]>a[j+1]){
                t=a[j];a[j]=a[j+1];a[j+1]=t;
            }
    printf("从小到大为：\n");
    for (i=0;i<10;i++)
        printf("%d\n",a[i]);
    return 0;
}
