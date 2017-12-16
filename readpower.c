#include "readpower.h"
#include <stdio.h>
#include <stdlib.h>

int percoreDVFS(int core, int cmd)
{
	static char fpstr[64];
	int freq;
	FILE *proc_stat_fd;
	if(cmd==5) return 0;
	sprintf(fpstr,"/sys/devices/system/cpu/cpu%d/cpufreq/scaling_setspeed",core);
	if((proc_stat_fd=fopen(fpstr,"w"))==NULL)
	{
		printf("Cannot Open %s\n",fpstr);
		exit(-1);
	}
	switch(cmd)
	{
		case 4:freq=800000;break;
		case 3:freq=1000000;break;
		case 2:freq=1300000;break;
		case 1:freq=1500000;break;
		case 0:freq=1900000;break;
		default:printf("Set unavailable Freq to core");return -1;
	}
	fprintf(proc_stat_fd,"%d",freq);
	fclose(proc_stat_fd);
	return 0;
}

int DVFS(int *coreLevel)
{
	int i;
	static int lastcoreLevel[CORE_NUM]={0,0};
	for(i=0;i<CORE_NUM;i++)
	{
		if(coreLevel[i]!=lastcoreLevel[i])
		{
			percoreDVFS(i,coreLevel[i]);
			lastcoreLevel[i]=coreLevel[i];
		}
	}
	return 0;
}

double GetAvgWatts()
{
	int i,j,n;
	static char buf[10240];
	char cmd[20]="#D,R,0";
	char* clearmen="#R,W,0";
	double watts=0;
	char WattsStr[102400];
	int count=0;
	double total=0;
	int fd=open(DEVICE,O_RDWR | O_NONBLOCK);
	n=write(fd,cmd,strlen(cmd));
	if(n!=strlen(cmd))
	{
		perror("Writing command failed!\n");
		exit(-1);
	}
	int retry=0;
	do
	{
		n=read(fd,buf,10240);
		retry++;
		if(retry>200)
			return -1;
	}while (n<0);
	if(n>2048)
	{
		write(fd,clearmem,strlen(clearmem));
	}
	for(i=0;i<n;i++)
	{
		if(buf[i]=='#')
		{
			if(buf[i+1]=='d')
			{
				j=0;
				while(buf[i+8]!=',')
				{
					WattsStr[j]=buf[i+8];
					j++;
					i++;
				}
				WattsStr[j]='\0';
				watts=(double)strtol(WattsStr,NULL,10);
				watts/=10;
				count++;
				total+=watts;
			}
		}
	}
	close(fd);
	static double last_sample=0;
	if(watts==0)
		watts=last_sample;
	last_sample=watts;
	return (watts>0)?watts:0;
}

int InitTTY(void)
{
	struct termios t;
	int ret,n;
	char* cmd="#L,W,3,I,_,1;";
	char* clearmem="#R,W,0;";
	char* memful_overwrite="#O,W,1,1";
	int fd=open(DEVICE, O_RDWR | O_NONBLOCK);
	fcntl(fd,F_SETFL,0);
	ret=tcgetattr(fd,&t);
	if(ret!=0)
	{
		perror("Am I here?");
		return -2;
	}
	cfmakeraw(&t);
	cfsetispeed(&t,BAUDRATE);
	cfsetospeed(&t,BAUDRATE);
	t.c_iflag|=IGNPAR;
	t.c_cflag&=~CSTOPB;
	t.c_cflag&=~CSIZE;
	t.c_cflag|=CS8;
	t.c_cflag|=(CLOCAL | CREAD);
	tcflush(fd,TCIFLUSH);
	ret=tcsetattr(fd,TCSANOW,&t);
	if(ret!=0)
	{
		perror("Setting terminal attributes\n");
		return -3;
	}
	write(fd,cmd,strlen(cmd));
	write(fd,clearmem,strlen(clearmem));
	write(fd,memful_overwrite,strlen(memful_overwrite));
	close(fd);
	system("echo userspace > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor");
	system("echo 1900000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_setspeed");
	printf("Finished init...\n");
	return 0;
}
