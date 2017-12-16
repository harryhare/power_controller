#include "readpower.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc,char *argv[])
{
	double Budget=atof(argv[1]);
	double pwr=0;
	int i,n=0;
	FILE *fptrout;
	int powerlevel=0;
	int coreLevel[CORE_NUM]={0,0};
	InitTTY();
	GetAvgWatts();
	sleep(2);
	GetAvgWatts();
	sleep(1);
	GetAvgWatts();
	sleep(1);
	GetAvgWatts();
	sleep(1);
	printf("Start:...\n");
	if((fptrout=fopen(argv[2],"w"))==NULL)
	{
		printf("Cannot open %s for writing trace!\n",argv[2]);
		exit(-1);
	}
	while(1)
	{
		pwr=GetAvgWatts();
		if(pwr>Budget && poweerlevel<4) powerlevel++;
		else if(pwr<Budget && powerlevel>0) powerlevel--;
		for(i=0;i<CORE_NUM;i++) coreLevel[i]=powerlevel;
		DVFS(coreLevel);
		fprintf(fptrout,"%d\t%.3lf\t%d\n",n,pwr,powerlevel);
		printf("%d\t%.3lf\t%d\n",n,pwr,powerlevel);
		n++;
		sleep(1);
		fflush(fptrout);
	}
	fclose(fptrout);
	return 0;
	fclose(fptrout);
	return 0;
}
