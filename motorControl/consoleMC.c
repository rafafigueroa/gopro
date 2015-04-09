#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <fcntl.h>

#include "motor.h"

FILE *fp, *fh;


void getBytes(int fh1, char *buf, int num)
{

	fgets(buf, 25,fh);
}
	
int main()
{

	int cmdCount = 0;

	char buf[50];// = "123456789012345"; //xxxxxx,0,0,0,0,0,0,0,0,0};
	int result;
	int spd;

	system("stty -F /dev/ttyMFD2 raw");
	initMotorControl();

	fh = fopen("/dev/ttyMFD2","rw");
	fp = fopen("log.txt","w+");

	if (!fp)
	{
		perror("Can't open log!");
		exit(-1);
	}

	printf("Entering main loop...\n");
	while (1)
	{
		fgets(buf, 25, fh);
		printf("[%i] Got:%s\n",++cmdCount, buf);
		if ( buf[0] == 'q')
			break;
		sscanf(buf, "%d", &spd);
		setMotorSpeed(1, spd);
		fprintf(fp, "	Passed: %s   Speed: %i\n", buf, spd);
		printf("	Passed: %s   Speed: %i\n", buf, spd);
	}

	fclose(fp);
	fclose(fh);
	system("stty -F /dev/ttyMFD2 cooked");
}
		
		
		
		
		
		
		
