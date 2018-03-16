#include<stdio.h>
#include<stdlib.h>

typedef struct rows {
	char *show;
	char *net;
	long total;
	long ad;
	float fall;
} row;

char** get_words(char *str) {
	char** words;
	int i, cap=1, j=0;
	words=(char **)malloc(4*sizeof(char **));
	for(i=0; *(str+i)!='\n'; i++) {
		if(*(str+i)==',') {
			
		}
	}
	return words;
}

int main(int argc, char **argv) {
	int i;
	FILE *f;
	char *str, *c;
	if(argc<2) {
		printf("No input provided.\n");
		return 1;
	}
	printf("Opening file %s\n", argv[1]);
	row *r;
	f=fopen(argv[1], "r");
	if(!f) {
		printf("File error.\n");
		return 2;
	}
	i=0;
	while(1) {
		r+=i;
		r=(row *)malloc(sizeof(row *));
		c=fgets(str, 1000, f);
		//x=fscanf(f, "%s,%s,%ld,%ld,%f\n", (r+i)->show, (r+i)->net, &((r+i)->total), &((r+i)->ad), &((r+i)->fall));
		//printf("%d\n",x);
		if(c==NULL) {
			printf("Done!\n");
			break;
		}
		printf("%d\n",i);
		//printf("%s\n",str);
		/*
		printf("%s\t%s\t%ld\t%ld\t%f\n",(r+i)->show,(r+i)->net,(r+i)->total,(r+i)->ad,(r+i)->fall);
		*/
		i++;
	}
	return 0;
}
