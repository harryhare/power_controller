#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HELLO_WORLD_SERVER_PORT 30002
#define BUFFER_SIZE 1024
#define FILE_NAME_MAX_SIZE 512

void helpfile();

int main(int argc,char **argv)
{
	if(argc!=3)
	{
		printf("Usage:./%s <ServerIPAddress> <Command>\n",argv[0]);
		exit(1);
	}
	
	char file_name[FILE_NAME_MAX_SIZE+1];
	bzero(file_name,FILE_NAME_MAX_SIZE+1);
	// printf("Input command on server of h for help:\t");
	file_name[0] = argv[2][0]; // scanf("%s",file_name);
	char buffer[BUFFER_SIZE];
	if(file_name[0]=='h')
		helpfile();
	else
	{
		struct sockaddr_in client_addr;
		bzero(&client_addr,sizeof(client_addr));
		client_addr.sin_family=AF_INET;
		client_addr.sin_addr.s_addr=htons(INADDR_ANY);
		client_addr.sin_port=htons(0);
		int client_socket=socket(AF_INET,SOCK_STREAM,0);
		if(client_socket<0)
		{
			printf("Create Socket Failed!\n");
			exit(1);
		}
		if(bind(client_socket,(struct sockaddr*)&client_addr,sizeof(client_addr)))
		{
			printf("Client Bind Port Failed!\n");
			exit(1);
		}
		struct sockaddr_in server_addr;
		bzero(&server_addr,sizeof(server_addr));
		server_addr.sin_family=AF_INET;
		if(inet_aton(argv[1],&server_addr.sin_addr)==0)
		{
			printf("Server IP Address Error!\n");
			exit(1);
		}
		server_addr.sin_port=htons(HELLO_WORLD_SERVER_PORT);
		socklen_t server_addr_length=sizeof(server_addr);
		if(connect(client_socket,(struct sockaddr*)&server_addr,server_addr_length)<0)
		{
			printf("Can not connect to %s!\n",argv[1]);
			exit(1);
		}
		bzero(buffer,BUFFER_SIZE);
		strncpy(buffer,file_name,strlen(file_name)>BUFFER_SIZE?BUFFER_SIZE:strlen(file_name));
		if(send(client_socket,buffer,BUFFER_SIZE,0)<0)
		{
			printf("Sending command Failed!\n");
			//break;
		}
		//if(file_name[0]=='0')
			//break;
		int length=0;
		length=recv(client_socket,buffer,BUFFER_SIZE,0);
		switch(file_name[0])
		{
			case('9'):printf("The CPU utilization is %s\n",buffer);
				FILE *fpUti;	
				char fileUti[] = "Uti/Uti000.txt";
				fileUti[7] = argv[1][11], fileUti[8] = argv[1][12], fileUti[9] = argv[1][13]; 
				if((fpUti=fopen(fileUti,"w"))==NULL){
					printf("Cannot open %s for writing Utilization!\n", fileUti);
					exit(2);
				}
				fprintf(fpUti,"%s\n", buffer);
				fclose(fpUti);
				break;
			case('t'):printf("The CPU temperature is %s\n",buffer);
				FILE *fpTem;	
				char fileTem[] = "Tem/Tem000.txt"; 
				fileTem[7] = argv[1][11], fileTem[8] = argv[1][12], fileTem[9] = argv[1][13];
				if((fpTem=fopen(fileTem,"w"))==NULL){
					printf("Cannot open %s for writing Temperature!\n", fileTem);
					exit(2);
				}
				fprintf(fpTem,"%s\n", buffer);
				fclose(fpTem);
				break;
			case('p'):printf("The power consumption is %s\n",buffer);break;
			case('f'):printf("The current CPU frequency is %s\n",buffer);break;
			case('a'):
				if(buffer[0]=='8')
					printf("The current cpu frequency is the maxmium!\n");
				else
					printf("Increase the CPU frequency to %s.\n",buffer);
				break;
			case('d'):
				if(buffer[0]=='9')
					printf("The current cpu frequency is the minmiun!\n");
				else
					printf("Decrease the CPU frequency to %s.\n",buffer);
				break;
			default:printf("Set CPU frequency to %s\n",buffer);break;
		}
		close(client_socket);
	}

	exit(0);
	return 0;
}

void helpfile()
{
	printf("\n'1':Set CPU Frequency to 450000.\n");
	printf("'2':Set CPU Frequency to 900000.\n");
	printf("'3':Set CPU Frequency to 1350000.\n");
	printf("'4':Set CPU Frequency to 1800000.\n");
	printf("'5':Set CPU Frequency to 2250000.\n");
	printf("'6':Set CPU Frequency to 2700000.\n");
	printf("'7':Set CPU Frequency to 3300000.\n");
	printf("'8':Set CPU Frequency to 3600000.\n");
	printf("'9':Get CPU Utilization.\n");
	printf("'t':Get CPU Temperature.\n");
	printf("'f':Get current CPU frequency.\n");
	printf("'p':Get CPU power consumption.\n");
	printf("'a':Increase CPU frequency.\n");
	printf("'d':Decrease CPU frequency.\n");
	printf("'0':Quit!\n");
}
