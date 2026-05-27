#include<stdio.h>

int main(void){
    FILE *in_file,*out_file;
    int bufSize = 256;
    char buf[bufSize];

    in_file = fopen("sprite_character_mage_equipment_avatar_coat.NPK","rb");
    out_file = fopen("abc.NPK","wb");
    fseek(in_file,0,SEEK_END);

    int bufSizegth = ftell(in_file);
    int index = 0;
    int c;
    while(!fseek(in_file,index,SEEK_SET)){
        index += bufSize;
        if(index >= bufSizegth){
            index -= bufSize;
            fread(buf,bufSizegth - index,1,in_file);
            fwrite(buf,bufSizegth - index,1,out_file);
			break;
		}
		fread(buf,bufSize,1,in_file);
		fwrite(buf,bufSize,1,out_file);
    }
}
