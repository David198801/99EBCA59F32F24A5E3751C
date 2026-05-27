#include <stdio.h>
int main()
{
    int i,j,t,m,k;
    int a[10];
    printf("输入10个数字：\n");
    for (i=0;i<10;i++)
        scanf("%d",&a[i]);
    for (i=0;i<9;i++){
        k=a[i];
        for (j=i+1;j<10;j++){
            if (k>a[j]){
                k=a[j];t=j;
            }
        }
        a[t]=a[i];a[i]=k;
    }
    printf("从小到大为：\n");
    for (i=0;i<10;i++)
        printf("%d\n",a[i]);
    return 0;
}
