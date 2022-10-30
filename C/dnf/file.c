#include <stdio.h>
#include <string.h>
#include <math.h>
#include <io.h>
#include <sys/stat.h>

int getImgNum(FILE *file){
    int i;
    unsigned char buf[20];
    fread(buf,20,1,file);
    char header[16];
    int img_sum;
    memcpy(header,buf,1*16);
    if (strcmp(header, "NeoplePack_Bill") == 0){
        img_sum=0;
        for(i=19;i>15;i--){
            img_sum += buf[i]*pow(256,i-16);
        }
        return img_sum;
    }
}


void mkdirs(char *muldir)
{
    int i,len;
    char str[512];
    strncpy(str, muldir, 512);
    len=strlen(str);
    for( i=0; i<len; i++ )
    {
        if( str[i]=='/' )
        {
            str[i] = '\0';
            if( access(str,0)!=0 )
            {
                mkdir(str);
            }
            str[i]='/';
        }
    }
    if( len>0 && access(str,0)!=0 )
    {
        mkdir(str);
    }
}

void writeImg(char file[]){
    FILE *in_file,*out_file;
    int bufSize = 256;
    int buf_offset;
    int img_sum,img_num;
    int i;
    unsigned char buf[bufSize];



    in_file = fopen(file,"rb");

    img_sum = getImgNum(in_file);

    unsigned int offset,img_size;
    unsigned char img_table[264];
    char img_name[256];
    char count_str[256] = "puchikon@neople dungeon and fighter DNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNFDNF";

    for(img_num=0;img_num<img_sum;img_num++){
        fseek(in_file,20+img_num*264,SEEK_SET);
        fread(img_table,264,1,in_file);

        offset=0;
        for(i=3;i>=0;i--){
            offset += img_table[i]*pow(256,i);
        }

        img_size=0;
        for(i=7;i>3;i--){
            img_size += img_table[i]*pow(256,i-4);
        }

        for(i=0;i<255;i++){
            img_name[i] = img_table[i+8]^count_str[i];
        }
        img_name[255] = '\0';

        int img_path_num;
        char img_path[256];
        for(i=255;i>=0;i--){
            if(img_name[i] == '/')
                break;
        }
        strncpy(img_path,img_name,i);
        img_path[i]='\0';
        mkdirs(img_path);

        char img_path_name[258] = "./";
        strcat(img_path_name,img_name);
        out_file = fopen(img_path_name,"wb");


        buf_offset = 0;
        while(!fseek(in_file,offset + buf_offset,SEEK_SET)){
            buf_offset += bufSize;
            if(buf_offset >= img_size){
                buf_offset -= bufSize;
                fread(buf,img_size - buf_offset,1,in_file);
                fwrite(buf,img_size - buf_offset,1,out_file);
                break;
            }
            fread(buf,bufSize,1,in_file);
            fwrite(buf,bufSize,1,out_file);
        }
        fclose(out_file);
        out_file = NULL;
    }
}

int main(int argc,char *argv[]){
    int i;
     for(i=1;i<argc;i++)
         writeImg(argv[i]);
    return 0;
}
