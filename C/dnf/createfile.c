#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void CreateMyFile(char * szFileName,long long fileSize)
{
    FILE* fp = fopen(szFileName, "wb+"); // 创建文件
    if(fp==NULL)
        printf("失败");
    else
    {

        char c[100]="sssssss";
        const fpos_t fileSizeT = fileSize-1;
        //fseek(fp, fileSizeT-1, SEEK_SET); // 将文件的指针 移至 指定大小的位百置
        fsetpos(fp, &fileSizeT);
        fwrite(&c,1,7,fp);
        fclose(fp);
    }
}


int main(void)
{
    int fileQuantity=1;
    int i;
    char fileName[256] = "test";
    char ext[10] = "txt";
    long long size=0;

    printf("输入文件数量:");
    scanf("%d",&fileQuantity);
    printf("输入文件大小(MB):");
    scanf("%lld",&size);



    size = size*1024*1024;
    for (i=0; i<fileQuantity; i++)
    {

        char code[10];
        char currentFileName[256];
        sprintf(code, "%d", i+1);
        strcpy(currentFileName,fileName);
        strcat(currentFileName,code);
        strcat(currentFileName,".");
        strcat(currentFileName,ext);
        CreateMyFile(currentFileName,size);
    }
    return 0;

}
