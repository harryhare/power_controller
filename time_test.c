#include<stdio.h>
#include<time.h>
int main()
{
int i=0;
int c=0;
time_t t0=time(0);
time_t t;
while(1){
    i++;
    if(i%5000000000==0){
        c++;
        i=0;
        t=time(0);
        //printf("%ld\n",(long)(t-t0));
        t0=t;
        break;
    }
}
return 0;
}
