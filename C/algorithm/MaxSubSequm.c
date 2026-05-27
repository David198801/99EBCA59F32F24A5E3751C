#include <stdio.h>
int MaxSubSequm1(int A[], int N)
{
    int ThisSum, MaxSum = -100;
    int i, j, k;
    for (i = 0; i < N; i++)  {  // i 是子列左端的位置
        for (j = i; j <= N; j++){ //j 是子列右端的位置
            ThisSum = 0;               //*
            for (k = i; k <= j; k++)   //*
                ThisSum += A[k];       //*
            if (ThisSum>MaxSum)  // 如果刚得到的子列和更大
                MaxSum = ThisSum; // 更新结果

        }

    }// 循环结束
    return MaxSum;
}

int MaxSubseqSum4(int A[], int N)
{
    int ThisSum, MaxSum;
    int i;
    ThisSum = 0;
    MaxSum = -100;
    for (i = 0; i < N; i++){
        ThisSum += A[i];//向右累加
        if (ThisSum>MaxSum)
            MaxSum = ThisSum; // 发现更大和则更新当前结果
        else if (ThisSum < 0)  // 如果当前子列和为负数
            ThisSum = 0; // 则不可能使后面部分和增大，抛弃之
    }
    return MaxSum;

}
int main(void)
{
    int seq[5] = {-1,-1,-1,-1,-2};
    int max1,max2;
    max1 = MaxSubseqSum4(seq,5);
    max2 = MaxSubSequm1(seq,5);
    printf("%d\n",max1);
    printf("%d",max2);
    return 0;
}
