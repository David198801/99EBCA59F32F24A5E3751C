#include <cstdio>


int main(){
    int num,a,b,c,i;
    scanf("%d",&num);
    int result[num];
    for (i=0;i<num;i++){
        scanf("%d %d %d",&a,&b,&c);
        result[i]=a+b>c?1:0;
    }
    for (i=0;i<num;i++){
        printf("Case #%d:%s\n",i+1,result[i]==1?"ture":"false");
    }
    return 0;
}
