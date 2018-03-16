#include<stdio.h>
#include<stdlib.h>

int main() {
	int i;
	FILE *f;
	char *str,*x,c,*s,*t;
	f=fopen("../data/data_022217_060617.csv","r");
	if(!f) {
		printf("File error.\n");
		return 1;
	}
	x=fgets(str,500,f);
	//fscanf(f, "%s %s %s %s,%s,%ld,%ld,%f\n",str,str,str,str,str,&x,&x,&y);
	printf("%s",str);
	i=0;
	do {
		do {
			if(str[i]==',') {
				printf("\n");
				*s='\0';
				break;
			} else {
				*s=str[i];
				printf("%c",str[i]);
			}
			i++;
			s+=1;
		} while(str[i]!='\n');
		printf("%c",str[i++]);
		printf("%s",s);
		break;
	} while(str[i]!='\n');
	return 0;
}
