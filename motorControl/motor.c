#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

FILE *mc;

void initMotorControl()
{

	system("stty -F /dev/ttyMFD1 speed 19200 raw"); //init port

	mc = fopen("/dev/ttyMFD1","rw+");
	if (!mc)
	{
		printf("Could not open motor controller!\n");
		exit(-1);
	}

	setbuf(mc, NULL); //disable buffering
}
	
void setMotorSpeed(int motor, int speed)
{
	unsigned char cmd[] = {0xC2, 0x00};
	unsigned char cmdStop[] = {0xC2, 0x00};

	speed = -speed;

	unsigned char spd;

	if (speed > 0 && speed < 25)
		speed = 25;
	if ( speed > -25 && speed < 0)
		speed = -25;

	if ( speed < 0 )
	{	
		spd = (unsigned char)(-speed);
		cmd[0] = 0xC1; //Reverse speed
	}
	else
		spd = (unsigned char)speed;

	cmd[1] = spd;
	//for (speed = 0; speed < 50; speed++)
	fwrite(cmd, 1, 2, mc);
	fflush(mc);
	usleep(15000);
	fwrite(cmdStop, 1,2, mc);
	fflush(mc);
	
}


