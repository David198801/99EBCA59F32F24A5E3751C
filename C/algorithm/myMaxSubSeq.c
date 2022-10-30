#include<stdio.h>
int MaxSubSeq1(int seq[],int n){
    int thisSeq,maxSeq=0;
    int i,j;
    for (i=0;i<n;i++){
        thisSeq=0;
        for(j=i;j<n;j++){
            thisSeq += seq[j];
            if (thisSeq>maxSeq)
                maxSeq=thisSeq;
        }
    }
    return maxSeq;
}
int MaxSubseqSum4(int A[], int N)
{
    int ThisSum, MaxSum;
    int i;
    ThisSum = 0;
    MaxSum = -100;
    for (i = 0; i < N; i++){
        ThisSum += A[i];//向右累加
        if (ThisSum>MaxSum){
            MaxSum = ThisSum; // 发现更大和则更新当前结果
            printf("%d\n",MaxSum);}
        if (ThisSum < 0)  // 如果当前子列和为负数
            ThisSum = 0; // 则不可能使后面部分和增大，抛弃之
    }
    return MaxSum;

}

int Max3( int A, int B, int C ){ /* 返回3个整数中的最大值 */
    return A > B ? A > C ? A : C : B > C ? B : C;
}

int DivideAndConquer( int List[], int left, int right ){ /* 分治法求List[left]到List[right]的最大子列和 */
    int MaxLeftSum, MaxRightSum; /* 存放左右子问题的解 */
    int MaxLeftBorderSum, MaxRightBorderSum; /*存放跨分界线的结果*/

    int LeftBorderSum, RightBorderSum;
    int center, i;

    if( left == right )  { /* 递归的终止条件，子列只有1个数字 */
        //if( List[left] > 0 )
        return List[left];
        //else return 0;
    }

        /* 下面是"分"的过程 */
    center = ( left + right ) / 2; /* 找到中分点 */
        /* 递归求得两边子列的最大和 */
    MaxLeftSum = DivideAndConquer( List, left, center );
    MaxRightSum = DivideAndConquer( List, center+1, right );

        /* 下面求跨分界线的最大子列和 */
    MaxLeftBorderSum = -100; LeftBorderSum = 0;
    for( i=center; i>=left; i-- ) { /* 从中线向左扫描 */
        LeftBorderSum += List[i];
        if( LeftBorderSum > MaxLeftBorderSum )
                MaxLeftBorderSum = LeftBorderSum;
    } /* 左边扫描结束 */

    MaxRightBorderSum = -100; RightBorderSum = 0;
    for( i=center+1; i<=right; i++ ) { /* 从中线向右扫描 */
        RightBorderSum += List[i];
        if( RightBorderSum > MaxRightBorderSum )
                MaxRightBorderSum = RightBorderSum;
    } /* 右边扫描结束 */

        /* 下面返回"治"的结果 */
    return Max3( MaxLeftSum, MaxRightSum, MaxLeftBorderSum + MaxRightBorderSum );
}

int MaxSubseqSum3( int List[], int N ){ /* 保持与前2种算法相同的函数接口 */
        return DivideAndConquer( List, 0, N-1 );
    }



int main(void){
    int a[5]={-1,-5,-10,-6,-3};
    int b[3]={-3,1,3};
    int max;
    max = MaxSubseqSum3(a,5);
    printf("%d",max);
    return 0;
}
