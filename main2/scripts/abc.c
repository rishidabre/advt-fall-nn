#include<stdio.h>
#include<stdlib.h>

int main() {
	int i,j,cap;
	char *str="abcdefghijklmnopqrstuv";
	char *s, *t, *u;
	cap=1;
	s=(char *)malloc(cap*sizeof(char *));
	t=s;
	for(i=0; i<15; i++) {
		if(i>=cap) {
			u=(char *)realloc(s, cap*sizeof(char *));
			if(u==NULL) {
				printf("Error in reallloc.\n");
			}
			cap*=2;
			printf("Increaed capacity to %d\n",cap);
			s=u;
		}
		*(s+i)=str[i];
		printf("%c\n",*(s+i));
	}
	*(s+i)='\0';
	printf("'%s'\n",s);
}
