#include <stdio.h>
#include <string.h>
#define N 200
#define M 35

struct STD
{
	int sn;
	char name[10];
	char ans[50];
	int score;
	int rank;
}text[N];

int stdNum;

int input(char* fileName)
{
	FILE * fp;
	int i;
	fp = fopen(fileName,"r");
	if(!fp)
	{
		printf("无此文件\n");
		return -1;
	}
	for(i=0;i<N;i++)
	{
		if(3!=fscanf(fp,"%d%s%s",&text[i].sn,text[i].name,text[i].ans))
		{
			break;
		}
	}
	fclose(fp);
	return i;

}

void calcAns(char correctAns[]){
    int a,b,c,d,i,j;
    for (j=0;j<M;j++){
        for (a=b=c=d=0,i=0;i<stdNum;i++){
            switch (text[i].ans[j]){
                case 'A':a++;break;
                case 'B':b++;break;
                case 'C':c++;break;
                case 'D':d++;break;
                //case 'X':break;
            }
        }
        if(a>b&&a>c&&a>d)
            correctAns[j]='A';
        else if(b>a&&b>c&&b>d)
            correctAns[j]='B';
        else if(c>a&&c>b&&c>d)
            correctAns[j]='C';
        else if(d>a&&d>b&&d>c)
            correctAns[j]='D';
        }
}

void calcScore(char correctAns[]){
    int i,j,score;
    for (j=0;j<stdNum;j++){
        for (score=0,i=0;i<M;i++){
            if (text[j].ans[i]==correctAns[i]){
                if (i<15) score+=2;
                else if (i>=15&&i<25) score+=3;
                else if (i>=25&&i<M) score+=4;
            }

        }
        text[j].score=score;
    }
}

void calcFrequency(char correctAns[],int ansFrequency[]){
    int i,j,ansTimes;
    for (j=0;j<M;j++){
        for (ansTimes=0,i=0;i<stdNum;i++){
            if (text[i].ans[j]==correctAns[j])
                ansTimes++;
            }
        ansFrequency[j]=ansTimes;
        }

}

void calcOrder(int order[]){
    int i,j,t,k;
    for (i=0;i<stdNum;i++) order[i]=i;
    for (i=0;i<stdNum-1;i++){
        k=order[i];
        for (j=i+1;j<stdNum;j++){
            if (text[k].score>text[order[j]].score){
                k=order[j];
                t=j;
            }
        }
        order[t]=order[i];order[i]=k;
    }
    for (i=0;i<stdNum;i++)
        text[order[i]].rank=stdNum-i;
}

void printOrder(int order[],char key){
    int i,j,t;
    printf("名次\t学号\t   姓名\t      分数\n");
    if (key=='d'||key=='D')
        for (i=stdNum-1;i>=0;i--)
            printf("第%2d名\t%d\t%8s\t%d\n",stdNum-i,text[order[i]].sn,text[order[i]].name,text[order[i]].score);
    else if (key=='u'||key=='U')
        for (i=0;i<stdNum;i++)
            printf("第%2d名\t%d\t%8s\t%d\n",stdNum-i,text[order[i]].sn,text[order[i]].name,text[order[i]].score);
}

void output(){
    int i,max=0,min=100,scoreGrade[10]={0};
    float passNum=0.0,sum=0.0;
    FILE *fp;
    for (i=0;i<stdNum;i++){
        if (max<text[i].score) max=text[i].score;
        if (min>text[i].score) min=text[i].score;
        if (text[i].score>=60) passNum++;
        sum=sum+text[i].score;
        switch (text[i].score/10){
            case 0:scoreGrade[0]++;break;
            case 1:scoreGrade[1]++;break;
            case 2:scoreGrade[2]++;break;
            case 3:scoreGrade[3]++;break;
            case 4:scoreGrade[4]++;break;
            case 5:scoreGrade[5]++;break;
            case 6:scoreGrade[6]++;break;
            case 7:scoreGrade[7]++;break;
            case 8:scoreGrade[8]++;break;
            case 9:case 10:scoreGrade[9]++;break;
        }
    }
    fp=fopen("report.txt","w");
    fprintf(fp,"-----------------------------------------------------\n");
    fprintf(fp,"                    试卷分析\n");
    fprintf(fp,"最高分：%d  最低分：%d  平均分：%.2f\n",max,min,sum/stdNum);
    fprintf(fp,"及格率：%.2f%%\n",passNum/stdNum*100);
    fprintf(fp,"分数段人数：\n");
    for (i=0;i<9;i++)
        fprintf(fp,"%2d-%3d分 %d人\n",i*10,i*10+9,scoreGrade[i]);
    fprintf(fp,"%2d-100分 %d人\n",i*10,scoreGrade[i]);
    fprintf(fp,"-----------------------------------------------------\n\n\n");
    fprintf(fp,"成绩单\n\n学号\t   姓名\t      分数\t排名\n");
    for (i=0;i<stdNum;i++)
        fprintf(fp,"%d\t%8s\t%d\t第%2d名\n",text[i].sn,text[i].name,text[i].score,text[i].rank);
    fclose(fp);
}

void mainMenu(void){
    system("cls");
    printf("************************************************************\n\n");
    printf("                    按键选择菜单项\n\n");
    printf("    1:输出参考答案及频次      2:按姓名查询学生成绩\n");
    printf("    3:按成绩顺序输出名单      4:输出成绩单及试卷分析文件\n");
    printf("    0:退出\n\n");
    printf("************************************************************\n");
}

int main()
{
    int ansFrequency[M],order[N],i;
    char correctAns[M],filename[100],key,stdName[20];
    float correctRate[M];

    while (1){
        printf("请输入试卷文件名:\n");
        scanf("%s",filename);
        stdNum=input(filename);
        if (stdNum==-1)continue;
        else break;
    }

    stdNum=input(filename);
    calcAns(correctAns);
    calcScore(correctAns);
    calcFrequency(correctAns,ansFrequency);
    calcOrder(order);

    for (i=0;i<M;i++)
            correctRate[i]=ansFrequency[i]/(float)stdNum;

    while (1){
        mainMenu();
        key=getch();

        if (key=='1'){
        system("cls");

        for (i=0;i<M;i++)
            printf("第%d题\t答案%c  回答频次 %d次\t正确率%.2f%%\n",i+1,correctAns[i],ansFrequency[i],correctRate[i]*100);
        printf("\n\n按任意返回主菜单");
        getch();
        }

        else if(key=='2'){
            system("cls");
            printf("查询结束请输入quit返回主菜单\n\n");
            while (1){
                key=0;
                printf("请输入学生姓名：");
                scanf("%s",stdName);
                for (i=0;i<stdNum;i++)
                    if (strcmp(stdName,text[i].name) == 0){
                        printf("\n姓名：%s 成绩：%d\n\n",text[i].name,text[i].score);
                        key=1;
                        break;
                    }
                if (key==0)
                    printf("\n查无此人,请重新输入\n\n");
                if (strcmpi(stdName,"quit") == 0)
                    break;

            }
        }

        else if(key=='3'){
            system("cls");
            printf("按d由成绩降序排列，按u由成绩升序排列\n\n");
            key=getch();

                if (key!='u'&&key!='d'&&key!='U'&&key!='D'){
                    printf("输入错误，按任意返回主菜单\n");
                    getch();
					continue;

                }


            system("cls");
            printOrder(order,key);
            printf("\n\n按任意返回主菜单");
            getch();
        }

        else if(key=='4'){
            output();
            system("cls");
            printf("成绩单及试卷分析文件已保存到report.txt");
            printf("\n\n按任意返回主菜单");
            getch();
        }

        else if(key=='0') return 0;

        else ;

    }
}
