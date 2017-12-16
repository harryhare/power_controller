#ifndef READPOWER_H
#define READPOWER_H
#include <sys/time.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>

#define BAUDRATE B115200
#define DEVICE "/dev/ttyUSB0"
#define SAMPLING_TIME 1
#define TOTAL_COUNTS 10200
#define CORE_NUM 2
double GetAvgWatts();
int InitTTY();
int percoreDVFS(int core,int cmd);
int DVFS(int *coreLevel);
#endif
